from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('sms_man', views.sms_man, name='automaticSupSms_man'),
    path('get_smsmainNumber', views.get_smsmainNumber, name='get_smsmainNumber'),
    path('sup_smsmain', views.sup_smsmain, name='sup_smsmain'),
    path('sup_smsmain_getcode', views.sup_smsmain_getcode, name='sup_smsmain_getcode'),
#

]