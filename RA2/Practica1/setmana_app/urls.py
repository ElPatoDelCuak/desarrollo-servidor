from django.urls import path, register_converter
from . import views
from .converters import NegativeIntConverter
register_converter(NegativeIntConverter, 'negint')

urlpatterns = [
    path('', views.home, name='home'),
    path('<negint:day>/', views.dia, name='dia'),
]