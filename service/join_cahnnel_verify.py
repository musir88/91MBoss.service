import time
import re
from telethon.tl.functions.channels import LeaveChannelRequest
import os
import codecs
import time
import datetime

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
    userList = []
    # async for u in client.iter_participants('bs91m990', aggressive=True):
    # offset =
    # djafw
    # laoyingchuhai8
    # OKXGroup_CN
    # GT015

    # https: // t.me / xbzijian
    # https: // t.me / bz8822
    # https: // t.me / im0471

    channel = 'xbzijian'
    #
    # await client(LeaveChannelRequest(channel))
    # await asyncio.sleep(3)

    try:
        await client(JoinChannelRequest(channel))

    except Exception as e:
        await client.disconnect()
        print(str(e))

    await asyncio.sleep(3)

    try:
        photos = await client.get_messages(channel, 30)
    except Exception as e:
        await client.disconnect()
        print(str(e))


    for x in photos:
        # print(x)
        if hasattr(x, 'reply_markup') == True and x.reply_markup != None and x.mentioned == True:
            if len(x.reply_markup.rows) == 1:

                # 二次验证
                bot_buttons = x.reply_markup.rows[0].buttons[0]
                if str(bot_buttons).find("?") != -1 and hasattr(bot_buttons, 'url') == True:
                    await channel_SecondaryVerification(client, bot_buttons)
                    break





            # for r in enumerate(x.reply_markup.rows):
            #     for b_k, b in r.buttons:
            #         print(b)

            # print(x)
            # print(x.message)
            pass
    print("结束")

with client:
    client.loop.run_until_complete(main())