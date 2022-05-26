import time
import re

from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserProfilePhoto, ChannelParticipantsSearch,UserStatusRecently, Message
from telethon import TelegramClient
from telethon.tl.types import Channel, User, Chat
import pytz
from telethon.tl.functions.channels import GetChannelsRequest, GetFullChannelRequest, GetParticipantsRequest

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

async def get_participants(client, entity):
    participants = await client.get_participants(entity)
    participants_count = len(participants)
    participant_list = []
    # print("共有" + str(participants_count) + "名成员")
    for participant in participants:
        participant_info = save_user_info(participant)
        # print(participant_info)
        if participant_info['username']:
            participant_list.append(participant_info)
    # print(participant_list)
    print("共有" + str(participants_count) + "名成员")


api_id = 18806282
api_hash = '943cbfa09dd409ad53fba7ebce2ad477'
client = TelegramClient('91MBoss-session/919923144199', api_id, api_hash)


from telethon.tl.functions.channels import LeaveChannelRequest
import os
import codecs
import time
import datetime
import asyncio


async def send_Key_words(bot_name, Key_words):
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

async def Simple_filter_channels(bot_name):
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

async def extract_channel(bot_name, path):
    all_url = []
    while True:
        time.sleep(2)
        try:
            next_page = False
            photos = await client.get_messages(bot_name, 1)
            for x in photos:
                for u in x.entities:
                    if hasattr(u, 'url') == True:
                        print("正在提取：", u.url)
                        all_url.append(u.url)
                        fo = codecs.open(path, "a", 'utf-8')
                        fo.write(str(u.url) + "\n")
                        fo.close()

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
                "message": str(e)
            }

    return {
        "status": True,
        "message": "采集完成 → ( " + str(len(all_url)) + " )"
    }

async def main():
    userList = []
    # async for u in client.iter_participants('bs91m990', aggressive=True):
    Key_words = '图片'
    bot_name = "@hao1234bot"
    print("开始采集...")

    send_Key_words_result = await send_Key_words(bot_name, Key_words)
    if send_Key_words_result['status'] == False:
        print(send_Key_words_result)
        return send_Key_words_result

    time.sleep(2)
    print("粗略过滤频道...")

    Simple_filter_channels_result = await Simple_filter_channels(bot_name)
    if Simple_filter_channels_result['status'] == False:
        print(Simple_filter_channels_result)
        return Simple_filter_channels_result


    path = 'channel.txt'
    if os.path.exists(path) ==True:
        os.remove(path)

    time.sleep(2)
    print("开始提取链接...")

    extract_channel_result = await extract_channel(bot_name, path)
    print(extract_channel_result)

    await client.disconnect()



with client:
    client.loop.run_until_complete(main())