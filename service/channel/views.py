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


def channel_send(request):
    config_path = "91MBoss/config/channel_send.config.json"

    if request.method == 'POST':
        data = request.POST
        config = {
            'client_number': '',
            'sleep_time': data['sleep_time'],
            'is_fake_content': data['is_fake_content'],
            'fake_content_sleep_time': data['fake_content_sleep_time'],
            'StartGroupSendTask': data['StartGroupSendTask'],
            'automaticReply': data['automaticReply'],
        }
        set_config(config_path, config)
        return redirect('channel_send')

    context = {
        'latest_question_list': 'opio',
        'config': get_config(config_path),
    }
    # print(context)
    return render(request, 'channel/channel_send.html', {'context': context})



async def get_Channel(session):
    result = {}
    phone = session
    result['phone'] = phone
    result['path'] = "91MBoss-session/群发账号/"

    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        client = client_init2(result)
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 'TelegramClient')
        return result

    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 'client.connect')
        return result

    try:
        channel = []
        async for dialog in client.iter_dialogs():
            if dialog.is_channel == True:
                channel_son = {
                    'id': dialog.id,
                    'name': dialog.name,
                    'username': dialog.entity.username,
                }
                channel.append(channel_son)
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 'getChannel')
        return result

    await client.disconnect()
    return {
        "status": True,
        "channel": channel,
    }

    return True


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

    try:
        # 再删除当前目录
        if os.path.exists(path) == True:
            time.sleep(1)
            os.remove(path)

        return True
    except Exception as e:
        print("sremovesessionNumber2: "+str(e))


async def get_sendChannel(session):
    path = "91MBoss/CronTab/" + str(session) + ".json"
    # print(path)
    if not os.path.exists(path):
        # 更新已加入的群链接 get_channel
        channel = await get_Channel(session)
        if channel['status'] == False:
            return channel

        if len(channel['channel']) < 1:
            # 迁移至未加群 列表
            emptyChannel({
                'phone': str(session),
                "path": "91MBoss-session/群发账号/"
            })

            return {
                "status": False,
                "message": "没有加入任何聊天群",
            }

        channel_list = channel['channel']
        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps(channel_list))
        fo.close()

    f = open(path, encoding="utf-8")
    channel_list = f.read()
    f.close()

    channel_list = json.loads(channel_list)
    if len(channel_list) < 1:
        os.remove(str(path))
        return {
            "status": False,
            "message": "所有群已经发送完毕，下轮重新爬取已加入的群发消息",
        }

    # 取这次发的群
    random.shuffle(channel_list)
    channel = channel_list.pop()

    # 保存剩下得 群
    os.remove(str(path))
    fo = codecs.open(path, "a", 'utf-8')
    fo.write(json.dumps(channel_list))
    fo.close()

    return {
        "status": True,
        "channel": channel,
    }


async def automaticReply(session, reply_content):
    session = str(session)
    result = {
        "phone": session,
        "path": "91MBoss-session/群发账号/",
    }

    try:
        client = client_init2(result)
    except Exception as e:
        await client.disconnect()
        print("client_init2 " + str(e))
        result = await telethonErrorMessage(result, e)
        return result


    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()
        print("connect " + str(e))
        result = await telethonErrorMessage(result, e)
        return result



    try:
        dialog_list = client.iter_dialogs()
    except Exception as e:
        await client.disconnect()
        print("iter_dialogs " + str(e))
        result = await telethonErrorMessage(result, e, 'getChannel')
        return result

    try:
        get_me = await client.get_me()
    except Exception as e:
        await client.disconnect()
        print("get_me " + str(e))
        result = await telethonErrorMessage(result, e, 'get_me')
        return result


    async for dialog in dialog_list:

        # print(dialog)

        try:
            if dialog.is_user == True and dialog.entity.deleted == False and dialog.message.reply_to == None:

                if 777000 == int(dialog.message.peer_id.user_id):
                    continue

                if dialog.entity.bot == True:
                    continue

                if dialog.message.peer_id.user_id == get_me.id:
                    continue

                if dialog.message.from_id != None:
                    continue

                reply_result = await client.send_message(dialog.entity, reply_content)

                string = str(date.today()) + "\n咨询客户ID：" + str(dialog.message.peer_id.user_id) + " → " + str(dialog.entity.username)
                string = string + "\n咨询消息：" + str(dialog.message.message)
                string = string + "\n回复消息：" + str(reply_content)

                # 记录回复日志
                fo = codecs.open("log/自动回复日志/" + str(time.strftime("%Y-%m-%d")) + ".log", "a", 'utf-8')
                fo.write("\n\n=====================================================\n\n" + str(string))
                fo.close()

                string = str(date.today()) + "\n咨询客户ID：" + str(dialog.message.peer_id.user_id)
                # string = string + "\n咨询消息：" + event.message.message
                string = string + "\n回复消息：" + str(reply_content)

                # 记录回复日志·
                fo = codecs.open("log/自动回复日志/client/" + str(time.strftime("%Y-%m-%d")) + ".log", "a", 'utf-8')
                fo.write("\n\n=====================================================\n\n" + str(string))
                fo.close()
                await client.disconnect()

                return {
                    "status": True,
                    "message": "自动回复成功"
                }

        except Exception as e:
            await client.disconnect()
            result = await telethonErrorMessage(result, e)
            return result

    await client.disconnect()
    return {
        "status": True,
        "message": "没有客户咨询"
    }


async def channel_sendsubmit(request):
    data = request.POST

    if 'session_string' not in data:
        return HttpResponse(json.dumps({
            'status': False,
            'message': "session_string 空"
        }, ensure_ascii=False))

    # 读取配置文件信息
    try:
        config_path = "91MBoss/config/channel_send.config.json"
        config = get_config(config_path)
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "获取配置文件错误：" + str(e),
        }, ensure_ascii=False))


    # 本次发送的群
    try:
        channel = await get_sendChannel(data['session_string'])
        if channel['status'] == False:
            return HttpResponse(json.dumps(channel, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "获取本次发送的群错误：" + str(e),
        }, ensure_ascii=False))



    # 先自动回复客户咨询
    try:
        automaticReply_result = await automaticReply(str(data['session_string']), config['automaticReply'])
    except Exception as e:
        automaticReply_result = await telethonErrorMessage({
            "phone": str(data['session_string']),
            "path": "91MBoss-session/群发账号/",
        }, str(e))

        return HttpResponse(json.dumps({
            "status": False,
            "message": "自动回复错误：" + automaticReply_result['message'],
        }, ensure_ascii=False))







    # 本次发送的消息
    try:
        send_content = get_sendContent()
        if send_content['status'] == False:
            return HttpResponse(json.dumps(send_content, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "获取本次发送的广告词错误：" + str(e),
        }, ensure_ascii=False))

    param = {
        'session_string': data['session_string'],
        'channel': channel,
        'content': send_content['content']['message'],
        'is_fake_content': config['is_fake_content'],
        'fake_content_sleep_time': config['fake_content_sleep_time'],
        'fake_content': '你好',
    }
    try:
        result = await tg_sendMessage(param)
        if result['status'] == False:
            result['channel'] = channel
            # result['message'] = "【" + channel.channel.username + ":" + channel.channel.name + "】" + result['message']
            return HttpResponse(json.dumps(result, ensure_ascii=False))
    except Exception as e:

        return HttpResponse(json.dumps({
            "channel": channel,
            "status": False,
            "message": "群发失败：" + str(e),
        }, ensure_ascii=False))

    return HttpResponse(json.dumps({
        'status': True,
        'param': param,
        'message': "成功",
        'channel': channel,
        'content': send_content,
        'send_content': send_content['content']['message'],
    }, ensure_ascii=False))


async def tg_sendMessage(data):
    # print(data)

    phone = data['session_string']
    channel = data['channel']['channel']
    content = data['content']
    if "username" in channel and channel['username'] != None:
        channel = channel['username']
    else:
        if "entity" in channel:
            channel = channel['entity']
        else:
            channel = channel['id']

    if 'is_fake_content' not in data:
        data['is_fake_content'] = 2

    result = {}
    result['phone'] = phone
    result['channel'] = channel
    result['submit'] = 'send_message'

    is_fake_content = str(data['is_fake_content'])
    if is_fake_content == '1':
        fake_content = data['fake_content']
        send_content = fake_content
    else:
        send_content = content

    result['is_fake_content'] = is_fake_content
    result['path'] = "91MBoss-session/群发账号/"

    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 1008)
        return result

    try:

        if is_fake_content != '1':
            await client.send_message(channel, send_content)
        else:
            await client.send_message(channel, send_content)
    except Exception as e:

        del result['is_fake_content']

        try:
            if str(e).find("Chat admin privileges are required to do that in the specified chat") != -1:
                await client(LeaveChannelRequest(channel))

            if str(e).find("You can't write in this chat") != -1:
                await client(LeaveChannelRequest(channel))

            await client.disconnect()
            result = await telethonErrorMessage(result, e, 10010)
        except Exception as son_e:
            await client.disconnect()
            result = await telethonErrorMessage(result, e, 10010)

        return result

    # 如果不是伪内容 直接记录发送日志
    if is_fake_content == '1':

        send_log_cnotent = phone + " → " + str(channel) + " → " + send_content
        # self.send_log(send_log_cnotent, "伪内容")

        if 'fake_content_sleep_time' not in data:
            data['fake_content_sleep_time'] = 3

        time.sleep(int(data['fake_content_sleep_time']))
        get_me = await client.get_me()
        photos = await client.get_messages(channel, 10)
        for x in photos:
            # print(x.from_id)
            # print(x.from_id.user_id)
            if x.text == send_content and x.from_id.user_id == get_me.id:
                # 发送伪内容 并记录发送日志
                await client.edit_message(channel, x.id, content)

                send_log_cnotent = str(
                    time.strftime("%Y-%m-%d %H:%M:%S")) + " → " + phone + " → " + channel + " → " + content
                send_log(send_log_cnotent)

                send_log_cnotent = str(time.strftime("%Y-%m-%d %H:%M:%S")) + channel + " → " + content
                send_log(send_log_cnotent, 'client')

                break
            # print(x.text)

    else:
        # 记录发送日志
        send_log_cnotent = str(time.strftime("%Y-%m-%d %H:%M:%S")) + " → " + str(phone) + " → " + str(
            channel) + " → " + str(send_content)
        send_log(send_log_cnotent)

        send_log_cnotent = str(time.strftime("%Y-%m-%d %H:%M:%S")) + channel + " → " + send_content
        send_log(send_log_cnotent, 'client')

    await client.disconnect()
    result['status'] = True
    return result


def send_log(content, prefix=''):
    if prefix == '':
        path = "log/群发日志/"
    else:
        path = "log/群发日志/" + prefix + "/"

    path = path + str(date.today()) + ".log"

    fo = codecs.open(path, "a", 'utf-8')
    fo.write("\n" + content)
    fo.close()

    return True

def joinchannel_log(content):
    path = "log/加群日志/" + str(date.today()) + ".log"
    fo = codecs.open(path, "a", 'utf-8')
    fo.write("\n" + content)
    fo.close()

    return True



def get_sendContent():
    path = "Message/【群发广告词】"
    list = []
    for file in os.listdir(path):
        file_name = str(file)
        # file_name = re.sub(".json", "", file_name)
        list.append(file_name)

    if len(list) < 1:
        return {
            "status": False,
            "message": "没有设置群发广告词"
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


def set_channel_sendContent(path, content):
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


def channel_sendContent(request):
    path = "Message/【群发广告词】"

    if request.method == 'POST':
        data = request.POST
        content = {
            'message': data['content'],
        }
        set_channel_sendContent(path, content)
        return redirect('channel_sendContent')

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
    # print(context)
    return render(request, 'channel/channel_sendContent.html', {'context': context})


def channel_delContent(request):
    path = "Message/【群发广告词】/"
    data = request.GET
    path = path + str(data['name']) + ".json"

    if os.path.exists(path):
        os.remove(str(path))
    return redirect('channel_sendContent')



def channel_init():
    path = "91MBoss/data/channel.json"
    if not os.path.exists(path):
        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps([]))
        fo.close()

    path = "91MBoss/config/channel_join.config.json"
    if not os.path.exists(path):
        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps({
            "sleep_time":3,#等待时间
            "StartGroupJoinTask":'2',#任务执行开关 默认关闭
        }))
        fo.close()

    return True


def channel_join(request):
    channel_init()
    path = "91MBoss/config/channel_join.config.json"

    # print(request)

    if request.method == 'POST':
        os.remove(path)
        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps({
            "sleep_time": request.POST['sleep_time'],  # 等待时间
            "StartGroupJoinTask": request.POST['StartGroupJoinTask'],  # 任务执行开关 默认关闭
        }))
        fo.close()

        if os.path.exists("91MBoss/data/channel_join.json") == True:
            os.remove("91MBoss/data/channel_join.json")

        return redirect('channel_join')

    f = open(path, encoding="utf-8")
    channel_join_config = f.read()
    f.close()
    channel_join_config = json.loads(channel_join_config)

    context = {
        'channel_join_config': channel_join_config,
    }
    return render(request, 'channel/channel_join.html', {'context': context})


def channel_save(request):
    channel_init()
    path = "91MBoss/data/channel.json"


    if os.path.exists("91MBoss/data/channel_join.json") == True:
        os.remove("91MBoss/data/channel_join.json")


    if request.method == 'POST':
        channel_string = request.POST['channel']
        channel = []
        for i in channel_string.split("\n"):
            channel.append(i.replace("\r",''))
        os.remove(path)
        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps(channel))
        fo.close()

        return redirect('channel_save')

    f = open(path, encoding="utf-8")
    channel = f.read()
    f.close()
    channel = "\n".join(json.loads(channel))

    context = {
        'channel': channel,
    }
    return render(request, 'channel/channel_save.html', {'context': context})


async def get_joinChannel(session_string):
    phone = str(session_string)

    path = "91MBoss/data/channel_join.json"
    if not os.path.exists(path):
        f = open("91MBoss/data/channel.json", encoding="utf-8")
        channel_all = f.read()
        f.close()
        channel_all = json.loads(channel_all)
        if len(channel_all) < 1:
            return {
                "status":False,
                "message":"至少添加一条群链接"
            }

        fo = codecs.open(path, "a", 'utf-8')
        fo.write(json.dumps(channel_all))
        fo.close()

    # 取一条群链接
    f = open(path, encoding="utf-8")
    channel_all = f.read()
    f.close()
    join_channel_all = json.loads(channel_all)
    if len(join_channel_all) < 1:
        return {
            "status":False,
            "code":'empty_channel',
            "message":"已经加完一轮，需要重新开始请再次刷新当前页面"
        }


    # 取这次发的群
    random.shuffle(join_channel_all)
    channel = join_channel_all.pop()

    # 保存剩下得 群
    os.remove(str(path))
    fo = codecs.open(path, "a", 'utf-8')
    fo.write(json.dumps(join_channel_all))
    fo.close()

    return {
        "status": True,
        "channel": channel,
    }


async def channel_joinsubmit(request):
    data = request.POST




    if 'session_string' not in data:
        return HttpResponse(json.dumps({
            'status': False,
            'message': "session_string 空"
        }, ensure_ascii=False))


    # 本次加的群
    try:
        channel = await get_joinChannel(data['session_string'])
        if channel['status'] == False:
            return HttpResponse(json.dumps(channel, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "获取本次加的群错误：" + str(e),
        }, ensure_ascii=False))

    # 开始加群
    try:
        channel_result = await joinChannel(data['session_string'], channel['channel'])
        channel_result['channel'] == channel
        if channel_result['status'] == False:

            if str(channel_result['message']).find("A wait of") != -1:
                channel_result['message'] = "频繁 " + channel_result['message']
                channel_result['code'] = "Await"

            return HttpResponse(json.dumps(channel_result, ensure_ascii=False))
        return HttpResponse(json.dumps(channel_result, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(json.dumps({
            "channel": channel,
            "status": False,
            "message": "本次加群错误：" + str(e),
        }, ensure_ascii=False))



async def joinChannel(session, channel=''):
    phone = str(session)
    channel = str(channel)

    result = {}
    result['phone'] = phone
    result['channel'] = channel
    result['submit'] = 'join_channel'

    result['path'] = "91MBoss-session/加群帐号/"

    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 'connect')
        return result

    try:
        await client(JoinChannelRequest(channel))
        result['status'] = True

        joinlog_cnotent = str(time.strftime("%Y-%m-%d %H:%M:%S")) + " → " + phone + " → " + channel + " → 加群成功"
        joinchannel_log(joinlog_cnotent)
        result['message'] = joinlog_cnotent

    except Exception as e:
        await client.disconnect()

        result = await telethonErrorMessage(result, e, 'JoinChannelRequest')
        joinlog_cnotent = str(time.strftime("%Y-%m-%d %H:%M:%S")) + " → " + phone + " → " + channel + " → 加群失败："+result['message']
        joinchannel_log(joinlog_cnotent)

        result['message'] = result['message']
        return result

    await asyncio.sleep(2)

    is_VERIFY = False

    try:
        photos = await client.get_messages(channel, 30)
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, "破解群验证获取验证消息失败："+str(e))
        return result

    # try:
    for x in photos:
        if hasattr(x, 'reply_markup') == True and x.reply_markup != None and x.mentioned == True:
            # print(x.message)
            # 记录日志
            # 验证CHANNEL
            send_log_cnotent = phone + " → " + channel + "\n" + x.message + "\n"
            # verifychannellog(send_log_cnotent, admin)

            is_VERIFY = True


            if len(x.reply_markup.rows) == 1:
                result['verify'] = True

                if hasattr(x.reply_markup.rows[0].buttons[0], 'url') == True:
                    bot_url = x.reply_markup.rows[0].buttons[0].url

                    if str(bot_url).find("?") != -1:

                        boturl_array = str(bot_url).split("?")
                        Order = re.sub("=", " ", boturl_array[1])

                        # webbrowser.open("https://my.telegram.org?domain=policr_mini_bot&start=verification_v1_-1001354379829")
                        # 破解二次验证机器人   敲门砖
                        # await client.send_message(boturl_array[0], '/start '+str(bot_url).split("start=")[1])

                        try:
                            await client.send_message(boturl_array[0], "/" + Order)
                        except Exception as e:
                            await client.disconnect()
                            result = await telethonErrorMessage(result, e, 'channel多步验证开始发送命令 ①')
                            return result

                        try:
                            await asyncio.sleep(2)
                            bot_message = await client.get_messages(boturl_array[0], 3)
                        except Exception as e:
                            await client.disconnect()
                            result = await telethonErrorMessage(result, e, 'channel多步验证 ②')
                            return result

                        for botphotos_x in bot_message:

                            # 针对个别群破解
                            if str(botphotos_x.message).find('那条河流是在湖南境内的') != -1:
                                try:
                                    # print(botphotos_x.reply_markup.rows)
                                    # print(botphotos_x.reply_markup['rows'])
                                    rows = botphotos_x.reply_markup.rows
                                except Exception as e:
                                    await client.disconnect()
                                    result = await telethonErrorMessage(result, e, 'channel多步验证 ③')
                                    return result


                    # await x.click(0)

                    # https: // t.me / +nncvrweqRs44Y2Yx
                    # KeyboardButtonUrl(text='前往验证', url='https://t.me/+nncvrweqRs44Y2Yx') → https: // t.me / hugoblog
                else:
                    # print(str(x.reply_markup.rows[0].buttons[0]) + " → " + channel+ " → " + phone)
                    await x.click(0)
                break

            if len(x.reply_markup.rows) > 1:
                try:
                    if str(x.message).find("请按顺序点击") != -1:
                        message = str(x.message)
                        message = message.split("\n")
                        message = message.pop()

                        message = re.sub("（", "(", message)
                        message = re.sub("）", ")", message)
                        message = re.findall(r'[(](.*?)[)]', message)[0]
                        message = message.split("、")
                        # print(message)
                        for row_idx, row in x.reply_markup.rows:
                            for bottons in row.buttons:
                                for son_idx, son in message:
                                    if son == bottons.text:
                                        result['verify'] = True
                                        print(str(bottons.text) + " → " + channel)
                                        # asyncio.create_task(x.click(bottons.data))
                                        await asyncio.sleep(1)
                                        print(row_idx)
                                        print(son_idx)
                                        await x.click(row_idx, son_idx)
                                        # await x.click(bottons.data)
                except Exception as e:
                    await client.disconnect()
                    result = await telethonErrorMessage(result, e, '请按顺序点击-no')
                    return result

            # if is_VERIFY == False:
            #     # NOVERIFY_CHANNEL
            #     send_log_cnotent = channel
            #     NOVERIFY_CHANNEL(send_log_cnotent, admin)


    await client.disconnect()
    return result

