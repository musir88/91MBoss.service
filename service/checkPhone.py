import time
import re
from telethon.tl.functions.channels import LeaveChannelRequest
import os
import codecs
import time
import datetime
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest

from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserProfilePhoto, ChannelParticipantsSearch,UserStatusRecently, Message
from telethon import TelegramClient
from telethon.tl.types import Channel, User, Chat
import pytz
import asyncio
from telethon.tl.functions.channels import GetChannelsRequest, GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest


def change_timezone(datetime):
    return datetime.astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")



api_id = 18806282
api_hash = '943cbfa09dd409ad53fba7ebce2ad477'
client = TelegramClient('91MBoss-session/919923144199', api_id, api_hash)


async def channel_SecondaryVerification(client, bot_buttons):

    print("channel机器人按钮：", bot_buttons)
    bot_buttons = bot_buttons.url
    boturl_array = str(bot_buttons).split("?")
    os_order = re.sub("=", " ", boturl_array[1])

    print(boturl_array)
    print("命令：", os_order)

    # 与机器人进行交互 1
    try:
        await client.send_message(boturl_array[0], "/" + os_order)
    except Exception as e:
        await client.disconnect()
        print(str(e))
        return ''

    try:
        await asyncio.sleep(2)
        bot_message = await client.get_messages(boturl_array[0], 2)
    except Exception as e:
        await client.disconnect()
        print(str(e))

        return ''

    for botphotos_x in bot_message:
        print("channel机器人按钮：", botphotos_x)









async def main():

    channel = 'xbzijian'

    phone_num = '6282119272386'

    contact = InputPhoneContact(client_id=0, phone=phone_num, first_name="zhang{}",
                                last_name="san")
    try:
        result = await client(ImportContactsRequest(contacts=[contact]))
        # print(phone_num)
        print(result.stringify())
        users = result.users
        if len(users) > 0:
            print(phone_num + "已注册")
        else:
            print(phone_num + "未注册")
    except Exception as e:
        print(e)
        raise RuntimeError('检查api失败...')

    print("结束")

with client:
    client.loop.run_until_complete(main())