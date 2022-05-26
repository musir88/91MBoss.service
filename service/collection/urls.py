from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('collection_channelUser', views.collection_channelUser, name='collection_channelUser'),
    path('collection_channelUser_submit', views.collection_channelUser_submit, name='collection_channelUser_submit'),
    path('collection_channelUrl_submit', views.collection_channelUrl_submit, name='collection_channelUrl_submit'),
    path('collection_channelUrl', views.collection_channelUrl, name='collection_channelUrl'),
]