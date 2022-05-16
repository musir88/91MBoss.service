from django.shortcuts import render
from pathlib import Path
import os
import json
import codecs
import os
import re
import time
import random
from datetime import date, timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
# from TestModel.models import Test
import os
import shutil
import socks
import asyncio
from selectolax.parser import HTMLParser
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import LeaveChannelRequest
# Create your views here.


def get_config(path):
    f = open(path, encoding="utf-8")
    content = f.read()
    f.close()
    return json.loads(content)

def set_config(path, content):
    os.remove(path)
    fo = codecs.open(path, "a", 'utf-8')
    fo.write(json.dumps(content))
    fo.close()
    return True

def sms_man_sup(submit=''):
    return submit


def sms_man(request):
    path = "91MBoss/config/sup.smsman.json"
    if request.method == 'POST':
        data = request.POST
        config = {
            'SecretKey': data['SecretKey'],
        }
        set_config(path, config)
        return redirect('automaticSupSms_man')

    context = {
        "config":get_config(path)
    }

    return render(request, 'AutomaticSup/sms_man.html', {"context":context})


