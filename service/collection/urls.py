from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('collection_channelUser', views.collection_channelUser, name='collection_channelUser'),
    path('collection_channelUser_submit', views.collection_channelUser_submit, name='collection_channelUser_submit'),
]