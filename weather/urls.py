from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_summary, name='weather_summary'),
]
