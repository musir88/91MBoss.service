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
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest

# Create your views here.

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

def get_telethonapi():
    path = "91MBoss/config/api_config/"

    list = []
    for file in os.listdir(path):
        file_name = str(file)
        list.append(file_name)

    random.shuffle(list)
    content = list.pop()

    f = open(path + content, encoding="utf-8")
    content = f.read()
    content = json.loads(content)
    f.close()
    return content

def set_config(path, content):
    if os.path.exists(path) ==True:
        os.remove(path)
    fo = codecs.open(path, "a", 'utf-8')
    fo.write(json.dumps(content))
    fo.close()
    return True

def get_config(path):
    f = open(path, encoding="utf-8")
    content = f.read()
    f.close()
    return json.loads(content)



def client_init2(result):
    proxy_param = proxy_set()

    proxy = (socks.SOCKS5, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])
    # print(result)
    # print("client_init2:" + str(proxy_param))

    api_path = "91MBoss/config/api/"+str(result['phone'])+".json"
    if not os.path.exists(api_path):
        api_content = get_telethonapi()
        api_content['session_phone'] =result['phone']
        set_config(api_path, api_content)
    api_content = get_config(api_path)


    return TelegramClient(result['path'] + result['phone'], int(api_content['api_id']), str(api_content['api_hash']))



    # return TelegramClient(result['path'] + result['phone'], 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
    # return TelegramClient('session/' + result['phone'], 18252973, '7996fe1f8cd8223ddbca884fccdfa880', proxy=proxy)


def USER_BANNED_IN_CHANNEL(result):

    try:
        # path = "session/" + phone + ".session"
        phone = str(result['phone'])
        path = result['path'] + phone + ".session"
        # 复制到新目录
        shutil.copyfile(path, "91MBoss-session/群发禁言/" + phone + ".session")

        # 再删除当前目录
        if os.path.exists(path) == True:
            os.remove(path)
        return True
    except Exception as e:
        return False


def emptyChannel(result):
    # path = "session/" + phone + ".session"
    try:
        phone = str(result['phone'])
        path = result['path'] + phone + ".session"

        # 复制到新目录
        shutil.copyfile(path, "91MBoss-session/加群帐号/" + phone + ".session")

        # 再删除当前目录
        if os.path.exists(path) == True:
            os.remove(path)

        return True
    except Exception as e:
        return False


async def sremovesessionNumber(result):

    # path = "session/" + phone + ".session"
    phone = str(result['phone'])
    path = result['path'] + phone + ".session"
    try:
        # 复制到新目录
        # shutil.copyfile(path, "91MBoss-session/官方销号/" + phone + ".session")
        shutil.move(path, "91MBoss-session/官方销号/" + phone + ".session")
    except Exception as e:
        print("sremovesessionNumber1: "+str(e))

    return True

    # try:
    #     # 再删除当前目录
    #     if os.path.exists(path) == True:
    #         time.sleep(1)
    #         os.remove(path)
    #
    #     return True
    # except Exception as e:
    #     print("sremovesessionNumber2: "+str(e))

def setTwoway(result):

    try:
        phone = str(result['phone'])
        path = result['path'] + phone + ".session"
        # 复制到新目录
        shutil.copyfile(path, "91MBoss-session/私信双向/" + phone + ".session")

        # 再删除当前目录
        if os.path.exists(path) == True:
            os.remove(path)
        return True
    except Exception as e:
        return False


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
        result['result_code'] = 'del_table'

    if str(e).find("You're banned from sending messages in supergroups/channels") != -1:
        # del result['messageEnglish']
        result['message'] = '用户已被官方禁止公开发言'
        result['messageChinese'] = '用户已被官方禁止公开发言'
        result['result_code'] = 'del_table'

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

    if str(e).find("Too many requests") != -1:
        # del result['messageEnglish']
        result['message'] = '私信双向：'+str(e)
        result['messageChinese'] = '群组禁止访问'
        result['result_code'] = 'del_table'
        setTwoway(result)


    fo = codecs.open("91MBoss/error_log/" + str(date.today()) + ".log", "a", 'utf-8')
    fo.write("\n" + str(result))
    fo.close()

    # print(result)
    return result


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

# def get_config(path):
#     f = open(path, encoding="utf-8")
#     content = f.read()
#     f.close()
#     return json.loads(content)
#
# def set_config(path, content):
#     if os.path.exists(path) == True:
#         os.remove(path)
#     fo = codecs.open(path, "a", 'utf-8')
#     fo.write(json.dumps(content))
#     fo.close()
#     return True

def user_console(request):
    config_path = "91MBoss/config/user_send.config.json"

    if request.method == 'POST':
        data = request.POST
        config = {

            'sleep_time': data['sleep_time'],#间隔时间
            'is_fake_content': data['is_fake_content'],
            'fake_content_sleep_time': data['fake_content_sleep_time'],
            'StartGroupSendTask': data['StartGroupSendTask'],
            'bombingNum': data['bombingNum'],
            'numberNum': data['numberNum'],
        }
        set_config(config_path, config)
        return redirect('user_console')

    context = {
        'latest_question_list': 'opio',
        'config': get_config(config_path),
    }

    return render(request, 'user/user_console.html', {'context': context})

def get_PrivateLetterNumber(request):
    data = request.POST

    api_param = {}

    user= get_config("91MBoss/data/user.json")


    if "numberNum" not in data:
        api_param['numberNum'] = 5
    else:
        api_param['numberNum'] = int(data['numberNum'])




    session_number = []
    for file in os.listdir("91MBoss-session/私信账号"):
        file_name = str(file)

        if str(file_name).find('-journal') != -1:
            continue

        file_name = re.sub(".session", "", file_name)

        session_number.append({
            'session_string':file_name,
        })


    if len(session_number) > 1:
        random.shuffle(session_number)

    session_list = []
    for session in session_number:
        session_list.append(session)
        if len(session_list) >= api_param['numberNum']:
            break

    return HttpResponse(json.dumps({
        'status':True,
        'list':session_list,
        'user':user
    }, ensure_ascii=False))

def get_send_content():
    path = "Message/【私信广告词】"
    list = []
    for file in os.listdir(path):
        file_name = str(file)
        # file_name = re.sub(".json", "", file_name)
        list.append(file_name)

    if len(list) < 1:
        return {
            "status": False,
            "message": "没有设置私信广告词"
        }

    random.shuffle(list)
    content = list.pop()

    f = open(path + "/" + content, encoding="utf-8")
    content = f.read()
    content = json.loads(content)
    f.close()

    return {
        "status": True,
        "content": content
    }


async def privateLetter(api_param):

    phone = api_param['phone']
    username = api_param['username']
    content = api_param['content']


    if 'is_fake_content' not in api_param:
        api_param['is_fake_content'] = 2

    result = {}
    result['phone'] = phone
    result['username'] = username
    result['submit'] = 'send_message'

    is_fake_content = str(api_param['is_fake_content'])
    if is_fake_content == '1':
        fake_content = api_param['fake_content']
        send_content = fake_content
    else:
        send_content = content

    result['is_fake_content'] = is_fake_content
    result['path'] = "91MBoss-session/私信账号/"

    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 1008)
        return result

    try:
        if is_fake_content != '1':
            await client.send_message(username, send_content)
        else:
            await client.send_message(username, send_content)
    except Exception as e:

        del result['is_fake_content']

        try:
            if str(e).find("Chat admin privileges are required to do that in the specified chat") != -1:
                await client(LeaveChannelRequest(username))

            if str(e).find("You can't write in this chat") != -1:
                await client(LeaveChannelRequest(username))

            await client.disconnect()
            result = await telethonErrorMessage(result, e, 10010)
        except Exception as son_e:
            await client.disconnect()
            result = await telethonErrorMessage(result, e, 10010)

        return result

    # 如果不是伪内容 直接记录发送日志
    if is_fake_content == '1':

        send_log_cnotent = phone + " → " + str(username) + " → " + send_content
        # self.send_log(send_log_cnotent, "伪内容")

        if 'fake_content_sleep_time' not in api_param:
            api_param['fake_content_sleep_time'] = 3

        time.sleep(int(api_param['fake_content_sleep_time']))
        get_me = await client.get_me()
        photos = await client.get_messages(username, 5)
        for x in photos:

            if x.text == send_content and x.from_id.user_id == get_me.id:
                # 发送伪内容 并记录发送日志
                await client.edit_message(username, x.id, content)

                send_log_cnotent = str(
                    time.strftime("%Y-%m-%d %H:%M:%S")) + " → " + phone + " → " + username + " → " + content
                send_log(send_log_cnotent)

                send_log_cnotent = str(time.strftime("%Y-%m-%d %H:%M:%S")) + username + " → " + content
                send_log(send_log_cnotent, 'client')

                break
            # print(x.text)

    else:
        # 记录发送日志
        send_log_cnotent = str(time.strftime("%Y-%m-%d %H:%M:%S")) + " → " + str(phone) + " → " + str(
            username) + " → " + str(send_content)
        send_log(send_log_cnotent)

        send_log_cnotent = str(time.strftime("%Y-%m-%d %H:%M:%S")) + username + " → " + send_content
        send_log(send_log_cnotent, 'client')

    await client.disconnect()
    result['status'] = True
    return result




async def user_sendsubmit(request):


    data = request.POST
    string = str(data['session']) + " → " + str(data['username'])

    try:
        # 广告词
        send_content = get_send_content()
        if send_content['status'] == False:
            string = string + " → " + str(send_content['message'])
        else:
            string = string + " → " + str(send_content['content']['message'])
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": False,
            "message": string + " → " + "获取私信广告词错误：" + str(e),
        }, ensure_ascii=False))


    fake_name = ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f','e', 'd', 'c', 'b', 'a'], random.randint(12,20)))

    try:
        config = get_config("91MBoss/config/user_send.config.json")

        api_param = {
            "phone": str(data['session']),
            "username": str(data['username']),
            "content": str(send_content['content']['message']),
            "fake_content": fake_name,  # 伪内容
            "is_fake_content": config['is_fake_content'],  # 伪内容开关
            "fake_content_sleep_time": config['fake_content_sleep_time'],  # 伪内容开关
        }
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": False,
            "message": string + " → " + "获取参数配置错误：" + str(e),
        }, ensure_ascii=False))


    # print(api_param)

    # 开始私信

    try:
        # 开始私信
        privateLetter_result = await privateLetter(api_param)
        if privateLetter_result['status'] == False:
            string = string + " → " + str(privateLetter_result['message'])
            privateLetter_result['message'] = string + " → " + "失败：" + str(privateLetter_result['message']),
        else:
            privateLetter_result['message'] = string
        return HttpResponse(json.dumps(privateLetter_result, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": False,
            "message": string + " → " + "失败：" + str(e),
        }, ensure_ascii=False))


def user_init():
    path = "91MBoss/data/user.json"
    if not os.path.exists(path):
        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps([]))
        fo.close()

    path = "91MBoss/config/user_send.config.json"
    if not os.path.exists(path):
        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps({
            "sleep_time": '8',
            "is_fake_content": '2',
            "fake_content_sleep_time": '2',
            "bombingNum": '2',  # 工作次数
            "StartGroupSendTask": '2',  # 启动任务
            "numberNum": '2',  # 启动任务
        }))
        fo.close()

    return True


def user_save(request):
    user_init()
    path = "91MBoss/data/user.json"

    if request.method == 'POST':
        channel_string = request.POST['user']
        channel = []
        for i in channel_string.split("\n"):
            channel.append(i.replace("\r", ''))
        os.remove(path)
        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps(channel))
        fo.close()

        return redirect('user_save')

    f = open(path, encoding="utf-8")
    channel = f.read()
    f.close()
    channel = "\n".join(json.loads(channel))

    context = {
        'user': channel,
    }
    return render(request, 'user/user_save.html', {'context': context})

def get_sendUser():

    path = "91MBoss/data/user.json"



def user_bombingMatch(request):

    data = request.POST
    # print(data)
    # print(data['num'])
    # print(data['session_list'])

    numberList = data['session_list']

    path = "91MBoss/data/user.json"

    numberList = numberList.split("==")

    session_list = []
    api_list = []
    for item in numberList:
        # print()

        # 获取私信对象
        username = user= get_config(path)

        if len(username) < 1:
            return HttpResponse(json.dumps({
                'status': False,
                "message":"全部私信完成/或用户库未放置私信用户"
            }, ensure_ascii=False))

        userItem= username.pop(0)

        item = item.split(",")
        api_param = {
            "username":userItem
        }
        set_config(path, username)

        for item_son in item:
            api_list.append({
                "session":item_son,
                "username":userItem,
            })
    #         print(api_param)
    #
    # print(api_list)

    return HttpResponse(json.dumps({
        'status':True,
        'api_list':api_list,
    }, ensure_ascii=False))


def send_log(content, prefix=''):
    if prefix == '':
        path = "log/私信日志/"
    else:
        path = "log/私信日志/" + prefix + "/"

    path = path + str(date.today()) + ".log"

    fo = codecs.open(path, "a", 'utf-8')
    fo.write("\n\n=====================================================\n\n" + content)
    fo.close()

    return True

async def addContacts(request):

    if request.method == 'POST':
        data = request.POST
    if request.method == 'GET':
        data = request.GET

    #     919901066213

    result = {}
    phone = str(data['phone'])
    result['phone'] = phone
    result['path'] = "91MBoss-session/私信账号/"
    contacts_numbere = data['contacts_numbere']

    try:
        client = client_init2(result)
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 'TelegramClient')
        return result

    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 'connect')
        return result

    last_name = "boss" + ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
         'f', 'e', 'd', 'c', 'b', 'a'], random.randint(1, 2)))

    contact = InputPhoneContact(client_id=0, phone=str(contacts_numbere), first_name=str(contacts_numbere), last_name=last_name)
    try:
        result = await client(ImportContactsRequest(contacts=[contact]))
        # print(result.stringify())
        users = result.users
        if len(users) > 0:
            return HttpResponse(json.dumps({
                "status": True,
                "message": contacts_numbere + " 添加成功",
            }, ensure_ascii=False))

            # print(contacts_numbere + " 已注册")
        else:
            # print(contacts_numbere + " 未注册")
            return HttpResponse(json.dumps({
                "status": False,
                "code": 'no_sup',
                "message": contacts_numbere + " 添加失败",
            }, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": False,
            "message": contacts_numbere + " 添加失败-：" + str(e),
        }, ensure_ascii=False))
