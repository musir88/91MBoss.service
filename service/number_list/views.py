from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
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
from telethon import TelegramClient, sync
from telethon.errors import SessionPasswordNeededError
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
        result['message'] = '掉线/或官方销号'
        result['messageChinese'] = str(e)
        await sremovesessionNumber(result)

    if str(e).find("Two-steps verification is enabled and a password is required") !=-1:
        result['message'] = '启用两步验证，需要密码:'+str(e)
        result['messageChinese'] = str(e)


    if str(e).find('The used phone number has been banned from Telegram and cannot be used anymore') != -1:
        # del result['messageEnglish']
        result['message'] = '掉线/或官方销号'
        result['messageChinese'] = str(e)
        await sremovesessionNumber(result)
        # USER_BANNED_IN_CHANNEL(result)

    if str(e).find('The key is not registered in the system') != -1:
        # del result['messageEnglish']
        result['message'] = '掉线/或官方销号'
        result['messageChinese'] = str(e)
        USER_BANNED_IN_CHANNEL(result)

    if str(e).find("You're banned from sending messages in supergroups/channels") != -1:
        # del result['messageEnglish']
        result['message'] = '官方禁发言'
        result['messageChinese'] = str(e)

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


async def sremovesessionNumber(result):
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
    result['path'] = "91MBoss-session/群发账号/"

    phone = request.GET['phone']
    phone = re.sub(".session", "", phone)
    result['phone'] = phone

    if not os.path.exists(result['path']+phone+".session"):
        result['path'] = "91MBoss-session/加群帐号/"

    if not os.path.exists(result['path']+phone+".session"):
        return HttpResponse(result['path']+phone+"群发账号、加群帐号 文件夹下都没有账号：" + phone)

    # print(result)

    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        # return HttpResponse(json.dumps(result, ensure_ascii=False))
        return HttpResponse(result['message'])

    try:
        photos = await client.get_messages(777000, 1)
        for x in photos:
            result['code'] = x.text
            continue
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(result['message'])
        # return HttpResponse(json.dumps(result, ensure_ascii=False))

    await client.disconnect()

    return HttpResponse(result['code'])

    # return HttpResponse(json.dumps({
    #     'status':True,
    #     'message':result['code']
    # }, ensure_ascii=False))


def get_joinchannel(request):
    session_number = []
    for file in os.listdir("91MBoss-session/加群帐号/"):
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


async def manual_login(request):
    session_number = ''
    verification_code = ''
    verification_code2 = ''
    message = ''
    phone_code_hash = ''
    password = ''

    if request.method == 'POST':
        data = request.POST
        session_number = data['session_number']
        verification_code = data['verification_code']
        password = data['password']
        phone = data['session_number']

        login_param = {
            "phone":session_number,
            "path":"91MBoss-session/手工登录/",
        }

        try:
            client = client_init2(login_param)
            # client = TelegramClient(login_param['path'] + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        except Exception as e:
            result = await telethonErrorMessage(login_param, e, "client_init2")
            # print(result)
            message = result['message']
            # return HttpResponse(result)

            context = {
                'session_number': session_number,
                'verification_code': verification_code,
                '2verification_code': verification_code2,
                'message': message,
                'phone_code_hash': phone_code_hash,
                'manual_login_ok': manual_login_ok,
            }
            return render(request, 'number_list/manual_login.html', {'context': context})

        try:
            await client.connect()
        except Exception as e:
            await client.disconnect()
            result = await telethonErrorMessage(login_param, e, "connect")
            # print(result)
            message = result['message']
            # return HttpResponse(result)
            context = {
                'session_number': session_number,
                'verification_code': verification_code,
                '2verification_code': verification_code2,
                'message': message,
                'phone_code_hash': phone_code_hash,
                'manual_login_ok': manual_login_ok,
            }
            return render(request, 'number_list/manual_login.html', {'context': context})

        if verification_code == '':
            try:
                await client.sign_in(phone=phone)
                sent = await client.send_code_request(phone)
                phone_code_hash = sent.phone_code_hash
                message = "验证码发送成功"
            except Exception as e:
                await client.disconnect()
                os.remove(login_param["path"] + phone + ".session")
                result = await telethonErrorMessage(login_param, e, "sign_in-sendcode")
                message = result['message']
        else:
            try:
                phone_code_hash = data['phone_code_hash']
                if password == "":
                    await client.sign_in(phone=phone, code=verification_code, phone_code_hash=phone_code_hash)
                else:
                    await client.sign_in(phone=str(phone), code=verification_code, password=str(password), phone_code_hash=str(phone_code_hash))
                message = "登录成功"
                await client.disconnect()
                shutil.copyfile("91MBoss-session/手工登录/" + phone + ".session", "91MBoss-session/手工登录/登录成功/" + phone + ".session")
            except SessionPasswordNeededError:

                try:
                    message = "登录成功"
                    me = await client.sign_in(password=password)
                    # 91MBoss-session/手工登录/登录成功
                    await client.disconnect()
                    shutil.copyfile("91MBoss-session/手工登录/" + phone + ".session", "91MBoss-session/手工登录/登录成功/" + phone + ".session")

                except Exception as e:
                    await client.disconnect()
                    result = await telethonErrorMessage(login_param, e, "sign_in-sendcode")
                    message = "登录失败:"+result['message']
            except Exception as e:
                await client.disconnect()
                result = await telethonErrorMessage(login_param, e, "sign_in-sendcode")
                message = "登录失败:" + result['message']




    context = {
        'session_number': session_number,
        'verification_code': verification_code,
        'password': password,
        'message': message,
        'phone_code_hash': phone_code_hash,
        'manual_login_ok': manual_login_ok,
    }
    return render(request, 'number_list/manual_login.html',  {'context': context})


def manual_login_ok():
    session_number = []
    for file in os.listdir("91MBoss-session/手工登录/登录成功/"):
        file_name = str(file)
        session_number.append({
            'session_string':file_name,
        })
    return session_number


def set_template(path="", content={}):
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

# 设置摸版

def template_manage(request):
    path = "91MBoss/template/"


    if request.method == 'POST':
        data = request.POST
        content = {
            'last_name': data['last_name'],
            'first_name': data['first_name'],
            'about': data['about'],
            'avatar': data['avatar'],
        }

        if content['last_name'] == '' and content['first_name'] == '' and content['about'] == '' and content['avatar'] == '':
            return redirect('template_manage')
        set_template(path, content)
        return redirect('template_manage')

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
            'last_name': content['last_name'],
            'first_name': content['first_name'],
            'about': content['about'],
            'avatar': content['avatar'],
        })

    avatar_list = []
    for file in os.listdir("91MBoss/template-avatar/"):
        avatar_list.append({
            "name": file,
            "path":"91MBoss/template-avatar/"+file
        })





    context = {
        'latest_question_list': 'opio',
        'list': list,
        'avatar_list': avatar_list,
        'content_count': len(list),
    }
    # print(context)
    return render(request, 'number_list/template_manage.html', {'context': context})


def template_manage_del(request):
    path = "91MBoss/template/"

    data = request.GET
    path = path + str(data['name']) + ".json"

    if os.path.exists(path):
        os.remove(str(path))
    return redirect('template_manage')












