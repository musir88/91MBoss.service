import time
import re

from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserProfilePhoto, ChannelParticipantsSearch,UserStatusRecently, Message
from telethon import TelegramClient
from telethon.tl.types import Channel, User, Chat
import pytz
from telethon.tl.functions.channels import GetChannelsRequest, GetFullChannelRequest, GetParticipantsRequest

def change_timezone(datetime):
    return datetime.astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")


api_id = 18806282
api_hash = '943cbfa09dd409ad53fba7ebce2ad477'
client = TelegramClient('91MBoss-session/6282113979952', api_id, api_hash)


from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
import os
import codecs
import time
import datetime
import asyncio
from telethon import events, Button

channel = 'https://t.me/bs91m991'

async def main():
    # await client(JoinChannelRequest('https://t.me/bs91m991'))

    await client.send_message('https://t.me/xoxoshe', '25')

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






    await client.disconnect()



with client:
    client.loop.run_until_complete(main())