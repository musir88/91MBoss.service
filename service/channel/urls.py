from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('channel_send', views.channel_send, name='channel_send'),
    path('channel_sendsubmit', views.channel_sendsubmit, name='channel_sendsubmit'),
    path('channel_join', views.channel_join, name='channel_join'),
    path('channel_sendContent', views.channel_sendContent, name='channel_sendContent'),
    path('channel_delContent', views.channel_delContent, name='channel_delContent'),
    path('channel_save', views.channel_save, name='channel_save'),
    path('channel_joinsubmit', views.channel_joinsubmit, name='channel_joinsubmit'),
    path('private_channel_save', views.private_channel_save, name='private_channel_save'),
    path('private_channel_console', views.private_channel_console, name='private_channel_console'),
    path('private_channel_joinSubmit', views.private_channel_joinSubmit, name='private_channel_joinSubmit'),


]