from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('user_advertiseContent', views.user_advertiseContent, name='user_advertiseContent'),
    path('user_delContent', views.user_delContent, name='user_delContent'),
    path('user_numberList', views.numberList, name='user_numberList'),
    path('user_console', views.user_console, name='user_console'),
    path('get_PrivateLetterNumber', views.get_PrivateLetterNumber, name='get_PrivateLetterNumber'),
    path('user_sendsubmit', views.user_sendsubmit, name='user_sendsubmit'),
    path('user_save', views.user_save, name='user_save'),
    path('user_bombingMatch', views.user_bombingMatch, name='user_bombingMatch'),
]