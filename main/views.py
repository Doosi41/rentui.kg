import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm

logger = logging.getLogger(__name__)


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            text = (
                f"Новое сообщение от {data['first_name']} {data['last_name']}\n\n"
                f"Email: {data['email']}\n"
                f"Телефон: {data['phone']}\n\n"
                f"Сообщение:\n{data['message']}"
            )

            try:
                send_mail(
                    subject="Новая заявка с сайта RentUi",
                    message=text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['altaiabdurahim07@gmail.com'],
                )
                messages.success(request, "Ваше сообщение успешно отправлено!")
                return redirect('contacts')
            except Exception:
                logger.exception("Не удалось отправить письмо с формы контактов")
                messages.error(request, "Не удалось отправить сообщение. Попробуйте позже.")
        else:
            messages.error(request, "Заполните имя, email и сообщение.")

    return render(request, 'main/contacts.html')

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')