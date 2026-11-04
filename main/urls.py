from django.urls import path
from . import views
from anons.views import property_list

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contacts/', views.contacts, name='contacts'),
    path('properties/', property_list, name='properties'),
]
