from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest


f = open('data/message.txt', encoding="utf-8")
message = f.read()
f.close()

# 导包
import os
import re
import time
import configparser
config = configparser.ConfigParser() # 类实例化

path = r'data/config.ini'
config.read(path)
api_id = config['base']['api_id']
api_hash = config['base']['api_hash']
phone = config['base']['phone']

print(config)
print(api_id)
print(api_hash)

session = ''
for file in os.listdir("session"):
    file_name = str(file)
    if str(file_name).find('-journal') != -1:
        continue
    session = re.sub(".session", "", file_name)
    break

if len(session) < 1:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "|", "session目录下没有可以提供使用的账号")
    input()
    os._exit(0)

print(time.strftime("%Y-%m-%d %H:%M:%S"), "|", "启动", session)


try:
    client = TelegramClient('session/'+str(phone), api_id, api_hash)
except Exception as e:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "|", session, "启动失败：", str(e))
    os._exit(0)




@client.on(events.ChatAction)
async def my_ChatAction(event):
    print(event)
    if event.user_joined:
        await event.reply(message)


client.start()
client.run_until_disconnected()