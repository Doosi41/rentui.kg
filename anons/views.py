from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from .forms import AnnouncementForm
from .models import AnnouncementImage, Announcement
from django.core.paginator import Paginator
from django.db.models import Q


# --- РЕГИСТРАЦИЯ И ВХОД ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('properties')
    else:
        form = UserCreationForm()
    return render(request, 'anons/sign-up.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли в аккаунт!")

            # Если на вход отправил @login_required, возвращаем туда, откуда пришёл.
            # Проверка нужна, чтобы через ?next= нельзя было увести на чужой сайт
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('properties')
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = AuthenticationForm()
    return render(request, 'anons/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта")
    return redirect('home')


@login_required
@require_POST
def property_delete(request, pk):
    property_item = Announcement.objects.filter(pk=pk).first()

    if not property_item:
        return redirect('properties')

    if property_item.author == request.user or request.user.is_superuser:
        property_item.delete()
        messages.success(request, "Объявление успешно удалено.")
    else:
        messages.error(request, "У вас нет прав на удаление этого объявления.")

    return redirect('properties')

@login_required
def create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')

        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user

            if images:
                announcement.image = images[0]

            announcement.save()

            for f in images[1:]:
                AnnouncementImage.objects.create(announcement=announcement, image=f)

            messages.success(request, "Объявление успешно создано!")
            return redirect('home')
        else:
            messages.error(request, "Проверьте правильность заполнения полей.")
    else:
        form = AnnouncementForm()

    return render(request, 'anons/create.html', {'form': form})
@login_required
def property_edit(request, pk):
    property_item = get_object_or_404(Announcement, pk=pk)

    if property_item.author != request.user and not request.user.is_superuser:
        messages.error(request, "У вас нет прав на редактирование.")
        return redirect('home')

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance=property_item)
        images = request.FILES.getlist('images')

        if form.is_valid():
            announcement = form.save(commit=False)

            if images:
                # старое главное фото больше не нужно — убираем его из хранилища
                if announcement.image:
                    announcement.image.delete(save=False)
                announcement.image = images[0]

            announcement.save()

            for f in images[1:]:                 # доливаем в галерею
                AnnouncementImage.objects.create(announcement=announcement, image=f)

            messages.success(request, "Объявление обновлено!")
            return redirect('home')
    else:
        form = AnnouncementForm(instance=property_item)

    return render(request, 'anons/create.html', {
        'form': form,
        'edit_mode': True,
        'property_item': property_item
    })


def property_list(request):
    # prefetch_related — чтобы фото галереи грузились одним запросом, а не отдельно на каждую карточку
    announcements = (
        Announcement.objects
        .select_related('author')
        .prefetch_related('images')
        .order_by('-id')
    )

    search_query = request.GET.get('search', '')
    if search_query:
        announcements = announcements.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Гость видит первые 5 объявлений, остальные — размытые заглушки (не больше 8)
    if not request.user.is_authenticated:
        total = announcements.count()
        return render(request, 'anons/property_list_guest.html', {
            'announcements': announcements[:5],
            'hidden_count': min(8, max(0, total - 5)),
            'total': total,
            'search_query': search_query,
        })

    paginator = Paginator(announcements, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'main/properties.html', {'page_obj': page_obj})
