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
    path('manual_login', views.manual_login, name='manual_login'),
    path('template_manage', views.template_manage, name='template_manage'),
    path('template_manage_del', views.template_manage_del, name='template_manage_del'),
    path('template_manage_console', views.template_manage_console, name='template_manage_console'),
    path('get_setTemplate', views.get_setTemplate, name='get_setTemplate'),
    path('setTemplate', views.setTemplate, name='setTemplate'),
    path('TemplateNumber_list', views.TemplateNumber_list, name='TemplateNumber_list'),
    path('client_number', views.client_number, name='client_number'),
    path('set_telethon_apidata', views.set_telethon_apidata, name='set_telethon_apidata'),
    path('telethon_delapiConfig', views.telethon_delapiConfig, name='telethon_delapiConfig'),

]