from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='number_index'),
    path('get_oknumber', views.get_oknumber, name='get_oknumber'),
]