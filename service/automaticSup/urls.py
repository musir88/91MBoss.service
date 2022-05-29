from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('sms_man', views.sms_man, name='automaticSupSms_man'),
    path('get_smsmainNumber', views.get_smsmainNumber, name='get_smsmainNumber'),
    path('sup_smsmain', views.sup_smsmain, name='sup_smsmain'),
    path('sup_smsmain_getcode', views.sup_smsmain_getcode, name='sup_smsmain_getcode'),
    path('automaticSup_api1', views.automaticSup_api1, name='automaticSup_api1'),
    path('get_automaticSup_api1Number', views.get_automaticSup_api1Number, name='get_automaticSup_api1Number'),
    path('sup_automaticSup_api', views.sup_automaticSup_api, name='sup_automaticSup_api'),
    path('sup_automaticSup_api_getcode', views.sup_automaticSup_api_getcode, name='sup_automaticSup_api_getcode'),
    path('automaticSup_ahasim', views.automaticSup_ahasim, name='automaticSup_ahasim'),
    path('get_supNumber', views.get_supNumber, name='get_supNumber'),
    path('sup_ahasim', views.sup_ahasim, name='sup_ahasim'),
    path('sup_ahasim_getcode', views.sup_ahasim_getcode, name='sup_ahasim_getcode'),
#

]