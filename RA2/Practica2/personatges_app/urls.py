from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #URL home per mostrar tots els personatges
    path('home/', views.home, name='home'),
    #URL que agafa el personatge a mostrar
    path('<str:personatge>/', views.personatge, name='personatge'),
]