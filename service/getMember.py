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

async def main():
    userList = []
    # async for u in client.iter_participants('bs91m990', aggressive=True):
    offset = 0
    limit = 200
    filter = []
    all_participants = []
    channel = 'BAOAA'
    channel = 'thecoinfarm'
    channel = 'bs91m990'
    channel = 'https://t.me/+sV8AzBkLm2pmYzdl'
    channel = 'sichouzhilu0'
    user_all = []

    # 是否过滤无头像 默认 1-过滤
    IS_FILTER_PHOTO = 1

    # ID长度过滤 超过则过滤
    ID_FILTER_LEN = 12

    # 是否采
    IS_SPECIFY_GROUP = 1

    # 时间过滤 默认采集3天内在线的
    TIME_FILTER_DAYS = 1
    TIMESTAMP_FILTER = 0
    # 先获得时间数组格式的日期
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=TIME_FILTER_DAYS))
    # 转换为时间戳
    TIMESTAMP_FILTER = int(time.mktime(threeDayAgo.timetuple()))
    # 转换为其他字符串格式
    # otherStyleTime = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
    # 注:timedelta()的参数有:days,hours,seconds,microseconds


    path = 'username.txt'
    if os.path.exists(path) ==True:
        os.remove(path)


    queryKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']
    for search_name in queryKey:
        offset = 0
        while True:
            participants = await client(GetParticipantsRequest(
                channel, ChannelParticipantsSearch(search_name), offset, limit,
                hash=0
            ))
            if not participants.users:
                break
            for user in participants.users:
                 participant_info = save_user_info(user)
                 if participant_info['username']:
                    if participant_info['username'] not in user_all:
                        print(participant_info['username'])

                        # 没有时间的过滤掉
                        if participant_info['status'] == None:
                            continue

                        # 时间不在范围内的过滤掉
                        status_time = time.strptime(str(participant_info['status']['time']), "%Y-%m-%d %H:%M:%S")
                        if int(time.mktime(status_time)) < TIMESTAMP_FILTER:
                            continue

                        # ID超过一定范围的过滤掉
                        if len(participant_info['username']) > ID_FILTER_LEN :
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
                        # fo.write(str(participant_info) + "\n")
                        fo.close()

            offset += len(participants.users)
            print(offset)

    print(channel + " → 数量："+str(len(user_all)))

    return ''

    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        entity = dialog.entity
        if isinstance(entity, Channel):
            entity = dialog.entity

            participants_count = entity.participants_count
            if participants_count >= 9000:
                participants_count = 9000
            try:
                # participants = await client.get_participants(entity=entity,aggressive=False)
                participants = await client.get_participants(entity=entity, limit=participants_count, aggressive=False)
                participants_count = len(participants)
                participant_list = []
                print(entity.username+":共有" + str(participants_count) + "名成员")
                for participant in participants:
                    participant_info = save_user_info(participant)
                    if participant_info['username']:
                        # print(participant_info)
                        participant_list.append(participant_info)
                # print(participant_list)
            except Exception as e:
                print('================')
                print(entity)
                print("错误："+str(e))
                print('================')


with client:
    client.loop.run_until_complete(main())