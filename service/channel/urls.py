from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('channel_send', views.channel_send, name='channel_send'),
    path('channel_sendsubmit', views.channel_sendsubmit, name='channel_sendsubmit'),
    path('channel_join', views.channel_join, name='channel_join'),
    path('channel_sendContent', views.channel_sendContent, name='channel_sendContent'),
    path('channel_delContent', views.channel_delContent, name='channel_delContent'),

]