from django import views
from django.shortcuts import render
# Create your views here.

class AutomaticSup(views.View):

    def sms_man(self, request):
        print("sms_man")

        return render(request, 'AutomaticSup/sms_man.html', {"context":{}})