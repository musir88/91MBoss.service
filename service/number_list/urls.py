from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='number_index'),
    path('number_nojoin', views.number_nojoin, name='number_nojoin'),
    path('number_jinyan', views.number_jinyan, name='number_jinyan'),
    path('number_xiaohao', views.number_xiaohao, name='number_xiaohao'),
    path('get_oknumber', views.get_oknumber, name='get_oknumber'),
    path('get_telegram_message', views.get_telegram_message, name='get_telegram_message'),
    path('get_joinchannel', views.get_joinchannel, name='get_joinchannel'),
]