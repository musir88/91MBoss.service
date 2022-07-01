import time
import re

from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserProfilePhoto, ChannelParticipantsSearch,UserStatusRecently, Message
from telethon import TelegramClient
from telethon.tl.types import Channel, User, Chat
import pytz
import os
from telethon.tl.functions.channels import GetChannelsRequest, GetFullChannelRequest, GetParticipantsRequest




def change_timezone(datetime):
    return datetime.astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")


api_id = 175132
api_hash = '2016997c709c95fc5577b49ea9a67be3'






client = TelegramClient('session/12567921572', api_id, api_hash, system_version='HTCDesire820G+dualsim', app_version="8.7.0 (26229)", device_model='Android 4.4.2 (KitKat)')


from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
import os
import codecs
import time
import datetime
import asyncio
from telethon import events, Button

# client = TelegramClient('session/12567921572', api_id, api_hash)






channel = 'https://t.me/bs91m991'

async def main():
    # await client(JoinChannelRequest('https://t.me/bs91m991'))

    # await client.send_message('https://t.me/xoxoshe', '25')

    # photos = await client.get_messages(channel, 10)
    # async for message in client.get_messages(channel, 10):
    #     print(message.id)
    #     # print(message.id, message.text)
    #     await client.forward_messages('https://t.me/xoxoshe', message.id, 'https://t.me/bs91m991')


    # for x in photos:
    #     print(x.id)
    #     # await client.forward_messages('xoxoshe', [x.id], channel,with_my_score=True)
    #     await client.forward_messages('xoxoshe', x, channel,with_my_score=True)
        # message = await client.send_message('https://t.me/xoxoshe',  "`coffrfrede`")
        # await client.pin_message('https://t.me/xoxoshe', message, notify=True)

        # await x.forward_to('https://t.me/xoxoshe',with_my_score =True, background=True, silent =True)

        # await client.send_message('https://t.me/xoxoshe', x)
    me = await client.get_me()

    print('me', me)


    async for dialog in client.iter_dialogs():
        if dialog.is_channel == True and dialog.entity.username != None:
            await client(LeaveChannelRequest(dialog.entity.username))
            print(dialog.entity.username)
        # print(dialog.entity)
    print('ok')

    await client.disconnect()



with client:
    client.loop.run_until_complete(main())