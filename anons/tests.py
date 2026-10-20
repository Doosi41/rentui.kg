from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Announcement

# В тестах файлы хранятся в памяти, чтобы ничего не улетало в DigitalOcean
TEST_STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}


def make_photo(name='photo.png'):
    buffer = BytesIO()
    Image.new('RGB', (1, 1)).save(buffer, 'PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


def announcement_data(**extra):
    data = {
        'title': 'Квартира в центре',
        'description': 'Две комнаты, рядом парк',
        'price': 25000,
        'phone': '555123456',
        'address': 'Бишкек',
    }
    data.update(extra)
    return data


@override_settings(STORAGES=TEST_STORAGES)
class AnnouncementTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('owner', password='pass12345')
        self.client.login(username='owner', password='pass12345')

    def test_first_photo_is_main_and_rest_go_to_gallery(self):
        photos = [make_photo(), make_photo(), make_photo()]
        self.client.post(reverse('create-anons'), announcement_data(images=photos))

        announcement = Announcement.objects.get()
        self.assertTrue(announcement.image)
        self.assertEqual(announcement.images.count(), 2)
        self.assertEqual(announcement.author, self.owner)

    def test_file_that_is_not_image_is_rejected(self):
        fake = SimpleUploadedFile('photo.png', b'this is not an image', content_type='image/png')
        response = self.client.post(reverse('create-anons'), announcement_data(images=[fake]))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Announcement.objects.exists())

    def test_photo_bigger_than_5mb_is_rejected(self):
        photo = make_photo()
        big_photo = SimpleUploadedFile('big.png', photo.read() + b'0' * 5 * 1024 * 1024, content_type='image/png')
        response = self.client.post(reverse('create-anons'), announcement_data(images=[big_photo]))

        self.assertContains(response, 'Максимальный размер фотографии')
        self.assertFalse(Announcement.objects.exists())

    def test_new_main_photo_replaces_old_one_in_storage(self):
        self.client.post(reverse('create-anons'), announcement_data(images=[make_photo()]))
        announcement = Announcement.objects.get()
        old_photo = announcement.image.name

        self.client.post(
            reverse('property_edit', args=[announcement.pk]),
            announcement_data(images=[make_photo('new.png')]),
        )

        announcement.refresh_from_db()
        self.assertNotEqual(announcement.image.name, old_photo)
        self.assertFalse(announcement.image.storage.exists(old_photo))

    def test_delete_works_only_with_post(self):
        announcement = Announcement.objects.create(author=self.owner, **announcement_data())
        url = reverse('property_delete', args=[announcement.pk])

        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertTrue(Announcement.objects.exists())

        self.client.post(url)
        self.assertFalse(Announcement.objects.exists())

    def test_cannot_delete_someone_elses_announcement(self):
        stranger = User.objects.create_user('stranger', password='pass12345')
        announcement = Announcement.objects.create(author=stranger, **announcement_data())

        self.client.post(reverse('property_delete', args=[announcement.pk]))

        self.assertTrue(Announcement.objects.exists())

    def test_cannot_edit_someone_elses_announcement(self):
        stranger = User.objects.create_user('stranger', password='pass12345')
        announcement = Announcement.objects.create(author=stranger, **announcement_data())

        self.client.post(
            reverse('property_edit', args=[announcement.pk]),
            announcement_data(title='Взломано'),
        )

        announcement.refresh_from_db()
        self.assertEqual(announcement.title, 'Квартира в центре')


@override_settings(STORAGES=TEST_STORAGES)
class PropertyListTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('owner', password='pass12345')
        for number in range(9):
            Announcement.objects.create(author=self.owner, **announcement_data(title=f'Квартира {number}'))

    def test_guest_sees_five_announcements_and_blurred_rest(self):
        response = self.client.get(reverse('properties'))

        self.assertTemplateUsed(response, 'anons/property_list_guest.html')
        self.assertEqual(len(response.context['announcements']), 5)
        self.assertEqual(response.context['hidden_count'], 4)

    def test_logged_in_user_sees_all_announcements(self):
        self.client.login(username='owner', password='pass12345')
        response = self.client.get(reverse('properties'))

        self.assertTemplateUsed(response, 'main/properties.html')
        self.assertEqual(len(response.context['page_obj']), 9)

    def test_search_by_title(self):
        response = self.client.get(reverse('properties'), {'search': 'Квартира 3'})

        self.assertEqual(response.context['total'], 1)


class AuthTests(TestCase):
    def setUp(self):
        User.objects.create_user('owner', password='pass12345')

    def test_login_returns_to_page_from_next(self):
        url = reverse('login') + '?next=' + reverse('create-anons')
        response = self.client.post(url, {'username': 'owner', 'password': 'pass12345'})

        self.assertRedirects(response, reverse('create-anons'))

    def test_login_ignores_next_to_another_site(self):
        url = reverse('login') + '?next=https://evil.com/'
        response = self.client.post(url, {'username': 'owner', 'password': 'pass12345'})

        self.assertRedirects(response, reverse('properties'))

    def test_logout(self):
        self.client.login(username='owner', password='pass12345')
        self.client.get(reverse('logout'))

        self.assertNotIn('_auth_user_id', self.client.session)
