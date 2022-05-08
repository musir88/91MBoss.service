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
        result['message'] = 'USER_DEACTIVATED_BAN'
        result['messageChinese'] = '用户已被删除/停用'
        path = "session/supok/" + result['phone'] + ".session"

        await sremovesessionNumber(result['phone'])

    if str(e).find('The used phone number has been banned from Telegram and cannot be used anymore') != -1:
        # del result['messageEnglish']
        result['message'] = 'USER_DEACTIVATED_BAN'
        result['messageChinese'] = '用户已被官方禁用'
        await sremovesessionNumber(result['phone'])

    if str(e).find('The key is not registered in the system (caused by ResolveUsernameRequest)') != -1:
        # del result['messageEnglish']
        result['message'] = 'USER_DEACTIVATED_BAN'
        result['messageChinese'] = '用户已被官方禁用'
        USER_BANNED_IN_CHANNEL(str(result['phone']))

    if str(e).find("You're banned from sending messages in supergroups/channels") != -1:
        # del result['messageEnglish']
        result['message'] = 'USER_BANNED_IN_CHANNEL'
        result['messageChinese'] = '用户已被官方禁止公开发言'

        # 转移到 禁用列表
        USER_BANNED_IN_CHANNEL(str(result['phone']))

    if str(e).find("You can't write in this chat") != -1:
        # del result['messageEnglish']
        result['message'] = 'CHANNEL_MUTE'
        result['messageChinese'] = '群组禁言'

    if str(e).find(
            "The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it") != -1:
        # del result['messageEnglish']
        result['message'] = 'CHANNEL_MUTE_ACCESS'
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
            'client_number': data['client_number'],
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


def channel_join(request):
    if request.method == 'GET':
        template = loader.get_template('channel/channel_join.html')
        context = {
            'latest_question_list': 'opio',
        }
        return HttpResponse(template.render(context, request))

    if request.method == 'POST':
        data = {}


async def get_Channel(session):
    result = {}
    phone = session
    result['phone'] = phone
    result['path'] = "91MBoss-session/群发账号/"

    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        client = client_init2(result)
    except Exception as e:
        result = await telethonErrorMessage(result, e, 'TelegramClient')
        return result

    try:
        await client.connect()
    except Exception as e:
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


def USER_BANNED_IN_CHANNEL(phone):
    path = "session/" + phone + ".session"

    # 复制到新目录
    shutil.copyfile(path, "91MBoss-session/群发禁言/" + phone + ".session")

    # 再删除当前目录
    if os.path.exists(path) == True:
        os.remove(path)

    return True


def emptyChannel(phone):
    path = "session/" + phone + ".session"

    # 复制到新目录
    shutil.copyfile(path, "91MBoss-session/待加群号/" + phone + ".session")

    # 再删除当前目录
    if os.path.exists(path) == True:
        os.remove(path)

    return True


def sremovesessionNumber(phone):
    path = "session/" + phone + ".session"

    # 复制到新目录
    shutil.copyfile(path, "91MBoss-session/官方销号/" + phone + ".session")

    # 再删除当前目录
    if os.path.exists(path) == True:
        os.remove(path)

    return True


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
            emptyChannel(str(session))

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
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return result

    try:
        dialog_list = client.iter_dialogs()
    except Exception as e:
        await client.disconnect()
        result = await self.telethonErrorMessage(result, e, 'getChannel')
        return result

    get_me = await client.get_me()

    async for dialog in dialog_list:

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

                await client.send_message(dialog.entity, reply_content)

                string = str(date.today()) + "\n咨询客户ID：" + str(
                    dialog.message.peer_id.user_id) + " → " + dialog.entity.username
                string = string + "\n咨询消息：" + str(dialog.message.message)
                string = string + "\n回复消息：" + str(reply_content)

                # 记录回复日志
                fo = codecs.open("log/" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".log", "a", 'utf-8')
                fo.write("\n\n=====================================================\n\n" + str(string))
                fo.close()

                string = str(date.today()) + "\n咨询客户ID：" + str(dialog.message.peer_id.user_id)
                # string = string + "\n咨询消息：" + event.message.message
                string = string + "\n回复消息：" + str(reply_content)

                # 记录回复日志·
                fo = codecs.open("log/client/" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".log", "a", 'utf-8')
                fo.write("\n\n=====================================================\n\n" + str(string))
                fo.close()

                await client.disconnect()
                return {
                    "status": True,
                    "message"："自动回复成功"
                }

                except Exception as e:
                await client.disconnect()
                result = await telethonErrorMessage(result, e)
                return result

        await client.disconnect()
        return {
            "status": True,
            "message"："没有客户咨询"
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

            # 先自动回复客户咨询
            try:
                config = automaticReply(data['session_string'], config_path['automaticReply'])
            except Exception as e:
                return HttpResponse(json.dumps({
                    "status": False,
                    "message": "自动回复错误：" + str(e),
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
                    result['message'] = "【" + channel.channel.username + ":" + channel.channel.name + "】" + result[
                        'message']
                    return HttpResponse(json.dumps(result, ensure_ascii=False))
            except Exception as e:
                return HttpResponse(json.dumps({
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

                send_log_cnotent = phone + " → " + channel + " → " + send_content
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



