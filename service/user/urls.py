from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('user_advertiseContent', views.user_advertiseContent, name='user_advertiseContent'),
    path('user_delContent', views.user_delContent, name='user_delContent'),
    path('user_numberList', views.numberList, name='user_numberList'),
]