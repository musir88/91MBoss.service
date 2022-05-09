from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import time
import random
from datetime import date, timedelta
import os
import codecs
import re
import json
import random
import shutil
import socks
from faker import Faker
from selectolax.parser import HTMLParser
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import LeaveChannelRequest


async def telethonErrorMessage(result={}, e='', code='1000'):
    result['code'] = code
    result['status'] = False
    result['messageEnglish'] = str(e)
    result['message'] = str(e)
    # if 'admin' not in result:
    #     result['admin'] = ''

    if str(e).find('The user has been deleted/deactivated') != -1:
        result['message'] = '用户已被删除/停'
        result['messageChinese'] = '用户已被删除/停用'
        path = "session/supok/" + result['phone'] + ".session"
        await sremovesessionNumber(result)

    if str(e).find('The used phone number has been banned from Telegram and cannot be used anymore') != -1:
        # del result['messageEnglish']
        result['message'] = '用户已被官方禁用'
        result['messageChinese'] = '用户已被官方禁用'
        await sremovesessionNumber(result)
        # USER_BANNED_IN_CHANNEL(result)

    if str(e).find('The key is not registered in the system (caused by ResolveUsernameRequest)') != -1:
        # del result['messageEnglish']
        result['message'] = '用户已被官方禁用'
        result['messageChinese'] = '用户已被官方禁用'
        USER_BANNED_IN_CHANNEL(result)

    if str(e).find("You're banned from sending messages in supergroups/channels") != -1:
        # del result['messageEnglish']
        result['message'] = '用户已被官方禁止公开发言'
        result['messageChinese'] = '用户已被官方禁止公开发言'

        # 转移到 禁用列表
        USER_BANNED_IN_CHANNEL(result)

    if str(e).find("You can't write in this chat") != -1:
        # del result['messageEnglish']
        result['message'] = '群组禁言'
        result['messageChinese'] = '群组禁言'

    if str(e).find(
            "The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it") != -1:
        # del result['messageEnglish']
        result['message'] = '群组禁止访问'
        result['messageChinese'] = '群组禁止访问'

    if str(e).find("Chat admin privileges are required to do that in the specified chat") != -1:
        # del result['messageEnglish']
        result['message'] = '在指定的聊天中执行此操作需要聊天管理员权限（例如，在不属于您的频道中发送消息），或用于频道或组的权限无效'
        result['messageChinese'] = '在指定的聊天中执行此操作需要聊天管理员权限（例如，在不属于您的频道中发送消息），或用于频道或组的权限无效'

    fo = codecs.open("91MBoss/error_log/" + str(date.today()) + ".log", "a", 'utf-8')
    fo.write("\n" + str(result))
    fo.close()

    # print(result)
    return result


def USER_BANNED_IN_CHANNEL(result):
    # path = "session/" + phone + ".session"
    phone = str(result['phone'])
    path = result['path'] + phone + ".session"
    # 复制到新目录
    shutil.copyfile(path, "91MBoss-session/群发禁言/" + phone + ".session")

    # 再删除当前目录
    if os.path.exists(path) == True:
        os.remove(path)

    return True


def emptyChannel(result):
    # path = "session/" + phone + ".session"
    phone = str(result['phone'])
    path = result['path'] + phone + ".session"

    # 复制到新目录
    shutil.copyfile(path, "91MBoss-session/加群帐号/" + phone + ".session")

    # 再删除当前目录
    if os.path.exists(path) == True:
        os.remove(path)

    return True


def sremovesessionNumber(result):
    # path = "session/" + phone + ".session"
    phone = str(result['phone'])
    path = result['path'] + phone + ".session"
    # 复制到新目录
    shutil.copyfile(path, "91MBoss-session/官方销号/" + phone + ".session")

    # 再删除当前目录
    if os.path.exists(path) == True:
        os.remove(path)

    return True



def proxy_set():
    proxy = [
        {'host': '216.185.47.218', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '50.114.107.228', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '50.114.107.105', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '216.185.46.220', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '154.16.150.211', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '50.114.107.226', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '50.114.107.104', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '216.185.46.23', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '50.114.107.223', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        {'host': '216.185.46.28', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
    ]
    return random.choice(proxy)


def client_init2(result):
    proxy_param = proxy_set()

    proxy = (socks.SOCKS5, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])
    # print(result)
    # print("client_init2:" + str(proxy_param))
    return TelegramClient(result['path'] + result['phone'], 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
    # return TelegramClient('session/' + result['phone'], 18252973, '7996fe1f8cd8223ddbca884fccdfa880', proxy=proxy)









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
    for file in os.listdir("91MBoss-session/加群帐号"):
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


async def get_telegram_message(request):
    result = {}
    phone = request.POST['phone']
    phone = re.sub(".session", "", phone)
    result['phone'] = phone

    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    try:
        photos = await client.get_messages(777000, 1)
        for x in photos:
            result['code'] = x.text
            continue
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    await client.disconnect()
    return HttpResponse(json.dumps({
        'status':True,
        'message':result['code']
    }, ensure_ascii=False))

