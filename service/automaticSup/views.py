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
    proxy = (socks.SOCKS5, "'216.185.46.23", "49161", 'tigerfpv', "V4LEgUcmy7")
    # proxy = (socks.SOCKS5, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])

    # print("client_init:"+str(proxy_param))
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
    fo.write({
        "api_id":int(result['api_id']),
        "api_hash":str(result['api_hash']),
    })
    fo.close()

    path = "91MBoss-session/自动注册"
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists("91MBoss-session/自动注册/注册成功"):
        os.mkdir("91MBoss-session/自动注册/注册成功")


    return TelegramClient(
        path+'/' + str(result['phone']),
        int(result['api_id']),
        str(result['api_hash'])
        # proxy=proxy
    )


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


def api_idhash():
    proxy = [
        {'api_id': 18806282, 'api_hash': 'cbfa09dd409ad53fba7ebce2ad477'},
        {'api_id': 15718961, 'api_hash': '6355e6f68264228fbf0bff8891ad0370'},
        {'api_id': 17345465, 'api_hash': '1fcfcffb77d010b5235b13e840a158ef'},
        {'api_id': 12971859, 'api_hash': '2f5003c9d36f74d32bbd252391a386f8'},
        {'api_id': 14545894, 'api_hash': '6d3d71e021a42cfe83f03c888f7a8c28'},
        {'api_id': 12564222, 'api_hash': 'e5f301c0c350c9a49b7adac287c3100f'},
        {'api_id': 13869498, 'api_hash': '3bb10d91b3b12994f3de37839fa98a3b'},
        {'api_id': 14849339, 'api_hash': '371ec4e9d10e482035d177cd2c55056e'},
        {'api_id': 15579305, 'api_hash': '5b139aeb5136fb5d794e9a3eb02d9397'},
    ]

    path = "91MBoss/config/api_config/"
    list = []
    for file in os.listdir(path):
        file_name = str(file)
        list.append(file_name)

    if len(list) < 1:
        return {
            "status": False,
            "message": "没有设置开发号",
            'api': ''
        }

    random.shuffle(list)
    content = list.pop()

    f = open(path + content, encoding="utf-8")
    content = f.read()
    content = json.loads(content)
    f.close()
    return {
        'status':True,
        'api':content
    }



def sms_man_rejectActivation(result):
    respose = result['api_respose'].split(":")
    # print(respose)
    # print(respose[1])
    api = "http://api.sms-man.com/stubs/handler_api.php"

    config = get_config("91MBoss/config/sup.smsman.json")
    api_param = {
        "action":"setStatus",
        "api_key":config['SecretKey'],
        "id":respose[1],
        "status":-1,
    }
    respose = requests.post(url=api, data=api_param, verify=False)
    respose = respose.text
    return respose



def error_response(result):
    result['submit_code'] = ''

    if str(result['message']).find("The used phone number has been banned from Telegram and cannot be used anymore") != -1 :
        result['submit_code'] = "close"
        result['message'] = "官方禁用 " + str(result['message'])

    if str(result['message']).find("A wait of") != -1:
        result['submit_code'] = "close"
        result['message'] = "开发号频繁 " + str(result['message'])

    if str(result['message']).find("Two-steps verification is enabled and a password is required") != -1:
        result['submit_code'] = "close"
        result['message'] = "启用两步验证，需要密码（由SignInRequest引起）" + str(result['message'])


    if str(result['message']).find("未出码") != -1:
        result['submit_code'] = "close"


    if result['submit_code'] == "close":
        if result['api_code'] == "sms-man":
            rejectActivation_respose = sms_man_rejectActivation(result)
            result['rejectActivation_respose'] = str(rejectActivation_respose)





    string = "【 "+str(time.strftime("%Y-%m-%d %H:%M:%S"))+" 】"
    for item in result:
        string = str(string) + "\n"+str(item)+" → " + str(result[item])



    fo = codecs.open("91MBoss/error_log/sup" + str(date.today()) + ".log", "a", 'utf-8')
    fo.write("\n\n=============================================\n\n" + str(string))
    fo.close()

    return result


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

    idhash = api_idhash()
    result = idhash['api']
    if idhash['status'] == False and request.method == 'GET':
        result['status'] = False
        context = {}
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    result['api_code'] = 'sms-man'

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
            'phone_code_hash': data['phone_code_hash']
        }
        result['phone_code_hash'] = api_data['phone_code_hash']
        # print(api_data)

        if "api_hash" in data:
            result['api_hash'] = data['api_hash']

        if "api_id" in data:
            result['api_id'] = data['api_id']


    context = {
        "api_data": api_data,
    }

    result['phone'] = api_data['phone']
    result['api_respose'] = api_data['api_respose']


    try:
        client = client_init(result)
    except Exception as e:
        result['status'] = False
        result['message'] = "client_init:"+str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result['status'] = False
        result['message'] =  "connect:"+str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    if str(api_data['sup_step']) == '1':
        try:
            sent = await client.send_code_request(result['phone'], force_sms=True)
            # print('===================================================')
            # print(sent)
            phone_code_hash = sent.phone_code_hash
            result['status'] = True
            result['phone_code_hash'] = phone_code_hash
            result['message'] = '发送验证码成功'
            context['result'] = result
            await client.disconnect()
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result = error_response(result)
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
                phone=result['phone'],
                phone_code_hash=api_data['phone_code_hash']
            )
            result['phone_code_hash'] = api_data['phone_code_hash']
            shutil.copyfile("91MBoss-session/自动注册/" + result['phone'] + ".session", "91MBoss-session/自动注册/注册成功/" + result['phone'] + ".session")
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result = error_response(result)
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
        result['message'] = "SUP-成功"
        result['submit_code'] = "close"
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
        # print(result[2])
        return HttpResponse(json.dumps({
            "status": True,
            "phone": result[2],
            "api_respose": respose,
            "message": str(country)+"账号:" + str(respose) ,
        }, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "没有账号:" + str(respose),
        }, ensure_ascii=False))


def sup_smsmain_getcode(request):
    data = request.POST
    timing = data['timing']
    api_respose = data['api_respose']

    if int(timing) >400:
        result = error_response({
            'api_code':"sms-man",
            'api_respose':str(api_respose),
            'message':str(api_respose)+" 取码400次未出码主动放弃",
        })

        return HttpResponse(json.dumps({
            "status": False,
            "submit_code": "close",
            "message": str(data['api_respose']) + " → " + str(result['message']),
        }, ensure_ascii=False))


    api_respose = api_respose.split(":")
    api_id = api_respose[1]

    config = get_config("91MBoss/config/sup.smsman.json")
    country_list = config['nation'].split(",")
    SecretKey = config['SecretKey']

    api = "https://api.sms-man.com/stubs/handler_api.php"
    api_param = {
        "id": api_id,
        "action": "getStatus",
        "api_key": SecretKey
    }
    respose = requests.post(url=api, data=api_param, verify=False)
    respose = respose.text

    if 'STATUS_CANCEL' == str(respose):

        result = error_response({
            'api_code':"sms-man",
            'api_respose':str(api_respose),
            'message':str(respose),
        })

        return HttpResponse(json.dumps({
            "status": False,
            "submit_code": "close",
            "message": str(data['api_respose'])+" 超时："+str(respose),
        }, ensure_ascii=False))

    if str(respose).find("STATUS_OK") != -1:
        result = respose.split(":")
        # print(result)
        return HttpResponse(json.dumps({
            "status": True,
            "message": str(data['api_respose']) + " ==> " + str(respose),
            "code": str(result[1]),
        }, ensure_ascii=False))

    return HttpResponse(json.dumps({
        "status": False,
        "message": str(data['api_respose'])+" 没有获取到: " + str(respose),
    }, ensure_ascii=False))

def automaticSup_api1(request):




    return render(request, 'AutomaticSup/automaticSup_api1.html', {"context": {

    }})

