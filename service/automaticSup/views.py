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
import requests
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






def client_init(result):
    proxy_param = proxy_set()
    proxy = (socks.SOCKS5, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])

    print("client_init:"+str(proxy_param))
    config = {}
    config['proxy'] = proxy
    config['api'] = {
        'api_id':int(result['api_id']),
        'api_hash':str(result['api_hash']),
    }
    path = "91MBoss/config/api/"+ str(result['phone']) +".json"
    if os.path.exists(path) == True:
        os.remove(path)

    fo = codecs.open(path, "a", 'utf-8')
    fo.write(str(config))
    fo.close()

    path = "91MBoss-session/自动注册"
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists("91MBoss-session/自动注册/注册成功"):
        os.mkdir("91MBoss-session/自动注册/注册成功")


    return TelegramClient(path+'/' + result['phone'], int(result['api_id']), result['api_hash'], proxy=proxy)


def proxy_set():
    proxy = [
        {'host': '216.185.47.218', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.228', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.105', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.220', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '154.16.150.211', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.226', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.104', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.23', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.223', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.28', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
    ]
    return random.choice(proxy)





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

async def sup_smsmain(request):
    result = {
        "api_id":"18806282",
        "api_hash":"943cbfa09dd409ad53fba7ebce2ad477",
    }

    if request.method == 'GET':
        data = request.GET
        api_data = {
            'phone': data['phone'],
            'api_respose': data['api_respose'],
            'sup_step': '1',
        }

    if request.method == 'POST':
        data = request.POST
        api_data = {
            'phone': data['phone'],
            'api_respose': data['api_respose'],
            'sup_step': '2',
            'code': data['code'],
        }

    context = {
        "api_data": api_data,
    }

    result['phone'] = api_data['phone']

    try:
        client = client_init(result)
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    try:
        await client.connect()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    if str(api_data['sup_step']) == '1':
        try:
            await client.send_code_request(result['phone'], force_sms=True)
            await client.disconnect()
            result['status'] = True
            result['message'] = '发送验证码成功'
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    if str(api_data['sup_step']) == '2':

        try:
            first_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(7, 13)))
            last_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(8, 15)))

            await client.sign_up(
                code=api_data['code'],
                first_name=first_name,
                last_name=last_name,
                phone=result['phone']
            )

        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})


        # 设置二次验证码
        try:
            await client.edit_2fa(new_password='91m123456')
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

        # 设置用户名
        try:
            username = "boss"+''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(6, 12)))
            await client(UpdateUsernameRequest(username))
            result['username'] = username
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

        await client.disconnect()
        result['status'] = True
        result['message'] = "成功"
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})


def sms_man(request):
    path = "91MBoss/config/sup.smsman.json"
    if request.method == 'POST':
        data = request.POST
        config = {
            'SecretKey': data['SecretKey'],
            'nation': data['nation']
        }
        set_config(path, config)
        return redirect('automaticSupSms_man')

    context = {
        "config":get_config(path)
    }

    return render(request, 'AutomaticSup/sms_man.html', {"context":context})


def get_smsmainNumber(request):

    config = get_config("91MBoss/config/sup.smsman.json")
    country_list = config['nation'].split(",")

    random.shuffle(country_list)
    country = country_list.pop()
    SecretKey = config['SecretKey']

    api = "https://api.sms-man.com/stubs/handler_api.php"
    api_param = {
        "ref":"xRMGluESoodc",
        "country":country,
        "service":"tg",
        "action":"getNumber",
        "api_key":SecretKey
    }

    respose = requests.post(url=api, data=api_param, verify=False)
    respose = respose.text

    if respose.find("ACCESS_NUMBER") != -1:
        result = respose.split(":")
        print(result[2])
        return HttpResponse(json.dumps({
            "status": True,
            "phone": result[2],
            "api_respose": respose,
            "message": "账号:" + str(respose),
        }, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "没有账号:" + str(respose),
        }, ensure_ascii=False))

