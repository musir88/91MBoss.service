from django.shortcuts import render
from pathlib import Path
import os
import json
import codecs
import os
import re
import time
import datetime
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

from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserProfilePhoto, ChannelParticipantsSearch,UserStatusRecently, Message
from telethon import TelegramClient
from telethon.tl.types import Channel, User, Chat
import pytz
from telethon.tl.functions.channels import GetChannelsRequest, GetFullChannelRequest, GetParticipantsRequest

BASE_DIR = Path(__file__).resolve().parent.parent

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



def client_init2(result):

    api_path = "91MBoss/config/api/"+str(result['phone'])+".json"
    if not os.path.exists(api_path):
        api_content = get_telethonapi()
        api_content['session_phone'] =result['phone']
        set_config(api_path, api_content)
    api_content = get_config(api_path)


    return TelegramClient(result['path'] + result['phone'], int(api_content['api_id']), str(api_content['api_hash']))


async def telethonErrorMessage(result={}, e='', code='1000'):
    result['code'] = code
    result['status'] = False
    result['messageEnglish'] = str(e)
    result['message'] = str(e)

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

    return result





def change_timezone(datetime):
    return datetime.astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")

def save_user_info(user):
    '''
    保存user信息
    :param user:
    :return:
    '''
    user_info = {
        "id": user.id,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "bot": user.bot,
        "photo": user.photo,
        "status": user.status
    }

    # 判断是否有头像
    photo = user_info["photo"]
    if photo:
        # print(photo)
        if isinstance(photo, UserProfilePhoto):
            user_info["photo"] = {
                "photo_id": photo.photo_id,
                "dc_id": photo.dc_id
            }
        else:
            user_info["photo"] = None

    # 判断status是否为空 在线时间 离线时间
    status = user_info["status"]
    if status:
        if isinstance(status, UserStatusOffline):
            user_info["status"] = {
                "was_online": change_timezone(status.was_online),
                "time": change_timezone(status.was_online),
            }
        elif isinstance(status, UserStatusOnline):
            user_info["status"] = {
                "expires": change_timezone(status.expires),
                "time": change_timezone(status.expires),
            }
        else:
            user_info["status"] = None
    else:
        user_info["status"] = None
    # return json.dumps(user_info, ensure_ascii=False)
    return user_info




def collection_channelUser(request):
    result_dir = str(BASE_DIR)+"91MBoss/采集结果/"
    collection_dir = str(BASE_DIR)+"91MBoss-session/采集账号/"

    context = {
        'latest_question_list': 'opio',
        'result_dir': result_dir,
        'collection_dir': collection_dir,
    }
    return render(request, 'collection/collection_channelUser.html', {'context': context})


async def SPECIFY_GROUP_COLLECTION(phone, CHANNEL, IS_FILTER_PHOTO, ID_FILTER_LEN, TIMESTAMP_FILTER):

    phone = str(phone)

    result = {
        "phone": phone,
        "path": "91MBoss-session/采集账号/",
        'message': "成功",
        'IS_FILTER_PHOTO': IS_FILTER_PHOTO,
        'ID_FILTER_LEN': ID_FILTER_LEN,
        'TIMESTAMP_FILTER': TIMESTAMP_FILTER,
        'CHANNEL': CHANNEL,
    }

    try:
        client = client_init2(result)
    except Exception as e:
        print("初始化失败： " + str(e))
        result = await telethonErrorMessage(result, e)
        return result

    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()
        print("连接失败 " + str(e))
        result = await telethonErrorMessage(result, e)
        return result


    path = "91MBoss/采集结果/用户ID/"+str(CHANNEL)+'.txt'
    if os.path.exists(path) ==True:
        os.remove(path)

    user_all = []
    limit = 200

    queryKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
    for search_name in queryKey:
        offset = 0
        while True:
            participants = await client(GetParticipantsRequest(
                CHANNEL, ChannelParticipantsSearch(search_name), offset, limit,
                hash=0
            ))
            if not participants.users:
                break
            for user in participants.users:
                 participant_info = save_user_info(user)
                 if participant_info['username']:
                    if participant_info['username'] not in user_all:
                        print("正在甄选 → ", participant_info['username'])

                        # 没有时间的过滤掉
                        if participant_info['status'] == None:
                            continue

                        # 时间不在范围内的过滤掉
                        status_time = time.strptime(str(participant_info['status']['time']), "%Y-%m-%d %H:%M:%S")
                        if int(time.mktime(status_time)) < TIMESTAMP_FILTER:
                            continue

                        # ID超过一定范围的过滤掉
                        if len(participant_info['username']) > ID_FILTER_LEN:
                            continue

                        # 头像是否过滤掉
                        if str(IS_FILTER_PHOTO) == '1' and participant_info['photo'] == None:
                            continue

                        # 过滤机器人
                        if participant_info['bot'] == True:
                            continue

                        user_all.append(participant_info['username'])

                        fo = codecs.open(path, "a", 'utf-8')
                        fo.write(str(participant_info['username']) + "\n")
                        fo.close()

            offset += len(participants.users)
            # print(offset)
    await client.disconnect()
    result['message'] = CHANNEL + "  →  采集完成，符合要求数量 ( " + str(len(user_all)) + " )"

    return result

def get_collectionSession():
    path = "91MBoss-session/采集账号/"
    list = []
    for file in os.listdir(path):
        file_name = str(file)
        file_name = re.sub(".session", "", file_name)
        file_name = re.sub("-journal", "", file_name)
        list.append(file_name)

    if len(list) < 1:
        return {
            "status": False,
            "message": "没有采集账号"
        }

    random.shuffle(list)
    phone = list.pop(0)

    return {
        "status": True,
        "phone": phone
    }


async def collection_channelUser_submit(request):
    channel = ''
    phone = ''

    req_data = {}
    if request.method == 'POST':
        req_data = request.POST
    if request.method == 'GET':
        req_data = request.GET


    phone = get_collectionSession()
    if phone['status'] == False:
        return phone
    if phone['status'] == True:
        phone = phone['phone']



    # 时间过滤 默认采集1天内在线的
    TIME_FILTER_DAYS = 1
    if 'TIME_FILTER_DAYS' in req_data:
        TIME_FILTER_DAYS = int(req_data['TIME_FILTER_DAYS'])
    TIMESTAMP_FILTER = 0
    # 先获得时间数组格式的日期
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=TIME_FILTER_DAYS))
    # 转换为时间戳
    TIMESTAMP_FILTER = int(time.mktime(threeDayAgo.timetuple()))


    # 是否指定 link
    IS_SPECIFY_GROUP = 1
    if 'IS_SPECIFY_GROUP' in req_data:
        IS_SPECIFY_GROUP = int(req_data['IS_SPECIFY_GROUP'])
        channel = str(req_data['CHANNEL'])
        channel = re.sub("\+", "", channel)
        channel = re.sub("https://t.me/", "", channel)
        channel = re.sub("@", "", channel)

    # ID长度过滤 超过则过滤
    ID_FILTER_LEN = 15
    if 'ID_FILTER_LEN' in req_data:
        ID_FILTER_LEN = int(req_data['ID_FILTER_LEN'])


    # 是否过滤无头像 默认 1-过滤
    IS_FILTER_PHOTO = 1
    if 'IS_FILTER_PHOTO' in req_data:
        IS_FILTER_PHOTO = int(req_data['IS_FILTER_PHOTO'])


    # print("时间：",TIME_FILTER_DAYS)
    # print("是否指定GROUP：",IS_SPECIFY_GROUP)
    # print("ID长度：",ID_FILTER_LEN)
    # print("头像：",IS_FILTER_PHOTO)
    # print("CHANNEL：",channel)


    if str(IS_SPECIFY_GROUP) == '1':

        try:
            result = await SPECIFY_GROUP_COLLECTION(
                phone,
                channel,
                IS_FILTER_PHOTO,
                ID_FILTER_LEN,
                TIMESTAMP_FILTER
            )
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            return HttpResponse(json.dumps({
                "status": False,
                "message": "错误：" + str(e),
            }, ensure_ascii=False))



    return HttpResponse(json.dumps({
        "channel": channel,
        "status": False,
        "message": "错误：",
    }, ensure_ascii=False))





async def send_Key_words(client, bot_name, Key_words):
    try:
        await client.send_message(bot_name,Key_words)
        return {
            "status":True,
            "message":'success'
        }
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }

async def Simple_filter_channels(client, bot_name):
    try:
        photos = await client.get_messages(bot_name, 1)
        for x in photos:
            for r_k, r in enumerate(x.reply_markup.rows):
                for b_k,b in enumerate(r.buttons):
                    if str(b.text).find("👥") != -1:
                        await x.click(r_k, b_k)
                        break
        return {
            "status":True,
            "message":'success'
        }
    except Exception as e:
        return {
            "status":True,
            "message":'success'
        }

async def extract_channel(client, bot_name, path):
    all_url = []

    Lasttime_string = ''

    while True:
        time.sleep(2)
        try:
            next_page = False

            photos = await client.get_messages(bot_name, 1)
            for x in photos:

                string = ''

                if hasattr(x, 'reply_markup') == False:
                    raise Exception("没有关键字相关链接1")
                if hasattr(x.reply_markup, 'rows') == False:
                    raise Exception("没有关键字相关链接2")


                for r_k, r in enumerate(x.reply_markup.rows):
                    for b_k,b in enumerate(r.buttons):
                        # print(b.text)
                        string = string+str(b.text)
                print("string → ", string)
                print("Lasttime_string → ", Lasttime_string)
                if string == Lasttime_string:
                    raise Exception("采集完成")
                Lasttime_string = string



                for u in x.entities:

                    if hasattr(u, 'url') == True:
                        # if all_url.count(u.url) > 0:
                        #
                        #     raise Exception("匹配到相同的数据退出采集")
                            # next_page = True
                            # break

                        print("正在提取：", u.url)
                        all_url.append(u.url)
                        fo = codecs.open(path, "a", 'utf-8')
                        fo.write(str(u.url) + "\n")
                        fo.close()

                if next_page == True:
                    next_page = False
                    break

                for r_k, r in enumerate(x.reply_markup.rows):
                    for b_k,b in enumerate(r.buttons):
                        # print(b)
                        if str(b.text).find("下一页") != -1:
                            # print(r_k, b_k, b.text)
                            next_page = True
                            await x.click(r_k, b_k)
                            continue
            if next_page == False:
                break

        except Exception as e:
            await client.disconnect()
            return {
                "status": False,
                "message":"采集完成 → ( " + str(len(all_url)) + " )" + str(e)
            }

    return {
        "status": True,
        "message": "采集完成 → ( " + str(len(all_url)) + " )"
    }






async def collection_channelUrl_submit(request):
    Key_words = ''
    phone = ''

    req_data = {}
    if request.method == 'POST':
        req_data = request.POST
    if request.method == 'GET':
        req_data = request.GET

    if 'Key_words' in req_data:
        Key_words = req_data['Key_words']
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "未指定关键词",
        }, ensure_ascii=False))

    if len(str(Key_words.strip)) < 1:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "未指定关键词",
        }, ensure_ascii=False))

    phone = get_collectionSession()
    if phone['status'] == False:
        return phone
    if phone['status'] == True:
        phone = phone['phone']

    result = {}
    result['phone'] = phone
    result['path'] = "91MBoss-session/采集账号/"

    try:
        client = client_init2(result)
    except Exception as e:
        print("初始化失败： " + str(e))
        result = await telethonErrorMessage(result, e)
        return result

    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()
        print("连接失败 " + str(e))
        result = await telethonErrorMessage(result, e)
        return result


    path = "91MBoss/采集结果/群链接/"+str(Key_words)+'.txt'
    # if os.path.exists(path) ==True:
    #     os.remove(path)



    # Key_words = '图片'
    bot_name = "@hao1234bot"
    print("开始采集...")

    send_Key_words_result = await send_Key_words(client, bot_name, Key_words)
    if send_Key_words_result['status'] == False:
        print(send_Key_words_result)
        return send_Key_words_result

    time.sleep(2)
    print("粗略过滤频道...")

    Simple_filter_channels_result = await Simple_filter_channels(client, bot_name)
    if Simple_filter_channels_result['status'] == False:
        print(Simple_filter_channels_result)
        return Simple_filter_channels_result

    # path = 'channel.txt'
    # if os.path.exists(path) ==True:
    #     os.remove(path)

    time.sleep(2)
    print("开始提取链接...")

    extract_channel_result = await extract_channel(client, bot_name, path)
    if extract_channel_result['status'] == True:
        await client.disconnect()
    extract_channel_result['message'] = str(Key_words) + " → " + str(extract_channel_result['message'])

    print(extract_channel_result)
    return HttpResponse(json.dumps(extract_channel_result, ensure_ascii=False))


def collection_channelUrl(request):
    print('collection_channelUrl')
    result_dir = str(BASE_DIR)+"91MBoss/采集结果/"
    collection_dir = str(BASE_DIR)+"91MBoss-session/采集账号/"



    context = {
        'latest_question_list': 'opio',
        'result_dir': result_dir,
        'collection_dir': collection_dir,
    }
    return render(request, 'collection/collection_channelUrl.html', {'context': context})