from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('sms_man', views.sms_man, name='automaticSupSms_man'),
#

]