from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest

# 导包
import os
import re
import time
import random
import asyncio
import shutil
import codecs
import configparser
config = configparser.ConfigParser() # 类实例化

path = r'Fur_config.ini'
config.read(path)
api_id = config['base']['api_id']
api_hash = config['base']['api_hash']
bot_phone = config['base']['bot_phone']
Fur_channel = config['base']['Fur_channel']
Fur_user = config['base']['Fur_user']

jiange_time1 = config['base']['jiange_time1']
jiange_time2 = config['base']['jiange_time2']


print(time.strftime("%Y-%m-%d %H:%M:%S"), "|", "账号：", bot_phone, '开始监听')


try:
    client = TelegramClient('session/'+str(bot_phone), api_id, api_hash)
except Exception as e:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "|", bot_phone, "监听失败：", str(e))
    os._exit(0)


async def client_init(session_string, api_id, api_hash):
    return TelegramClient('session/' + str(session_string), api_id, api_hash)


#
def errorHandling(s_string, error_e):

    log_string = str(error_e)

    if str(error_e).find("deleted/deactivated") != -1:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s_string, "] 官方销号")
        log_string = log_string + "\n"+s_string+":官方销号"


        shutil.copyfile("session/"+s_string+".session", "error-session/销号/" + s_string + ".session")
        if os.path.exists("session/"+s_string+".session") == True:
            os.remove("session/"+s_string+".session")

    fo = codecs.open("log/" + str(time.strftime("%Y-%m-%d")) + ".log", "a", 'utf-8')
    fo.write("\n\n=====================================================\n\n" + str(error_e))
    fo.close()


def get_session():
    session_list = []
    for file in os.listdir("session"):
        file_name = str(file)
        if str(file_name).find('-journal') != -1:
            continue
        file_name = re.sub(".session", "", file_name)

        if str(file_name) == bot_phone:
            continue
        session_list.append(file_name)
        # print(file_name)
    return session_list


async def FurFirst_start(s, peer):
    try:
        client_app = await client_init(s, api_id, api_hash)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] 开始登录")
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] 登录失败：", str(e))
        return ''

    try:
        await client_app.connect()
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] 登录成功")
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] 连接电报失败：", str(e))
        await client_app.disconnect()
        errorHandling(s, e)
        return ''

    config.read(r'Fur_config.ini')
    # F_data = config.read(path)
    ordermoney_string = config['Fur']['orderMoney']
    ordermoney_string = ordermoney_string.split(",")
    # money_string = config['Fur']['money']
    # money_string = money_string.split(",")

    if len(ordermoney_string) <= 0:
        # if len(order_string)<=0 or len(money_string) <=0:
        await client_app.disconnect()
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "|", "当前设置指令金额：", len(ordermoney_string), '个')
        # print(time.strftime("%Y-%m-%d %H:%M:%S"), "|","当前设置指令金额：", len(money_string), '个')
        return ''

    random.shuffle(ordermoney_string)
    ordermoney = ordermoney_string.pop()

    try:
        await client_app.send_message(peer, ordermoney)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] 下单成功", ordermoney)
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] 下单失败：", str(e), ordermoney)
        await client_app.disconnect()
        errorHandling(s, e)
        return ''
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] 退出登录：")
    await client_app.disconnect()
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] 退出成功：")
    return ''

async def Fur_start(peer):
    s_list = get_session()


    for s in s_list:

        jiange = random.uniform(int(jiange_time1), int(jiange_time2))
        time.sleep(jiange)

        await FurFirst_start(s, peer)


@client.on(events.NewMessage)
async def my_NewMessage(event):
    # print()
    # print(event.from_id)
    # print(event.message.message)
    e = await client.get_entity(event.from_id)
    # print("e.username:", e.username)
    # print("Fur_user:", Fur_user)
    if Fur_user == str(e.username):
        await Fur_start(event.peer_id)


client.start()
client.run_until_disconnected()



