from django.core import mail
from django.test import TestCase
from django.urls import reverse


class ContactsTests(TestCase):
    def test_message_is_sent_to_email(self):
        self.client.post(reverse('contacts'), {
            'first_name': 'Айбек',
            'email': 'aibek@gmail.com',
            'message': 'Хочу сдать квартиру',
        })

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Хочу сдать квартиру', mail.outbox[0].body)

    def test_empty_form_is_not_sent(self):
        self.client.post(reverse('contacts'), {})

        self.assertEqual(len(mail.outbox), 0)

    def test_wrong_email_is_not_sent(self):
        self.client.post(reverse('contacts'), {
            'first_name': 'Айбек',
            'email': 'не почта',
            'message': 'Привет',
        })

        self.assertEqual(len(mail.outbox), 0)
