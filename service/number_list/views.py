from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os
import re
import json
import random

def index(request):

    session_number = []
    for file in os.listdir("91MBoss-session/群发账号"):
        file_name = str(file)
        session_number.append({
            'session_string':file_name,
        })

    context = {
        'session_number': session_number,
        'session_number_count': len(session_number),
    }
    return render(request, 'number_list/index.html',  {'context': context})


def number_nojoin(request):

    session_number = []
    for file in os.listdir("91MBoss-session/待加群号"):
        file_name = str(file)
        session_number.append({
            'session_string':file_name,
        })

    context = {
        'session_number': session_number,
        'session_number_count': len(session_number),
    }
    return render(request, 'number_list/number_nojoin.html',  {'context': context})

def number_jinyan(request):

    session_number = []
    for file in os.listdir("91MBoss-session/群发禁言"):
        file_name = str(file)
        session_number.append({
            'session_string':file_name,
        })

    context = {
        'session_number': session_number,
        'session_number_count': len(session_number),
    }
    return render(request, 'number_list/number_jinyan.html',  {'context': context})

def number_xiaohao(request):

    session_number = []
    for file in os.listdir("91MBoss-session/官方销号"):
        file_name = str(file)
        session_number.append({
            'session_string':file_name,
        })

    context = {
        'session_number': session_number,
        'session_number_count': len(session_number),
    }
    return render(request, 'number_list/number_xiaohao.html',  {'context': context})



def get_oknumber(request):

    session_number = []
    for file in os.listdir("91MBoss-session/群发账号"):
        file_name = str(file)

        if str(file_name).find('-journal') != -1:
            continue

        file_name = re.sub(".session", "", file_name)

        session_number.append({
            'session_string':file_name,
        })

    if len(session_number) > 1:
        random.shuffle(session_number)

    return HttpResponse(json.dumps({
        'status':True,
        'list':session_number
    }, ensure_ascii=False))