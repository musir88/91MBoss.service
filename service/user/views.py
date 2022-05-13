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
from faker import Faker
from selectolax.parser import HTMLParser
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import LeaveChannelRequest

# Create your views here.

def set_sendContent(path, content):
    list = []
    for file in os.listdir(path):
        file_name = str(file)
        file_name = re.sub(".json", "", file_name)
        list.append(int(file_name))
    if len(list) < 1:
        path = path + "/1.json"
    else:
        path = path + "/" + str(max(list) + 1) + ".json"

    fo = codecs.open(path, "a", 'utf-8')
    fo.write(json.dumps(content, ensure_ascii=False))
    fo.close()

    return True


def user_advertiseContent(request):
    path = "Message/【私信广告词】"

    if request.method == 'POST':
        data = request.POST
        content = {
            'message': data['content'],
        }
        set_sendContent(path, content)
        return redirect('user_advertiseContent')

    list = []
    for file in os.listdir(path):
        file_name = str(file)
        file_name = re.sub(".json", "", file_name)

        f = open(path + "/" + file_name + ".json", encoding="utf-8")
        content = f.read()
        content = json.loads(content)
        f.close()

        list.append({
            "name": file_name,
            "content": content,
        })

    context = {
        'latest_question_list': 'opio',
        'list': list,
        'content_count': len(list),
    }
    return render(request, 'user/user_advertiseContent.html', {'context': context})


def user_delContent(request):
    path = "Message/【私信广告词】/"
    data = request.GET
    path = path + str(data['name']) + ".json"

    if os.path.exists(path):
        os.remove(str(path))
    return redirect('user_advertiseContent')

def numberList(request):
    print(5435)


    BASE_DIR = str(Path(__file__).resolve().parent.parent) + "91MBoss-session\私信账号"


    session_number = []
    for file in os.listdir("91MBoss-session/私信账号"):
        file_name = str(file)

        file_name_string = re.sub(".session", "", file_name)
        path_info = "91MBoss/data/TemplateInfo/"+str(file_name_string)+".json"
        if os.path.exists(path_info):
            f = open(path_info, encoding="utf-8")
            content = f.read()
            Template = json.loads(content)
            f.close()
        else:
            Template={
                "first_name":"",
                "last_name":"",
                "phone":"",
                "username":"",
            }

        session_number.append({
            'session_string':file_name,
            'Template':Template,
        })

    context = {
        'session_number': session_number,
        'session_number_count': len(session_number),
        'BASE_DIR': BASE_DIR,
    }
    # print(BASE_DIR)
    return render(request, 'user/numberList.html',  {'context': context})