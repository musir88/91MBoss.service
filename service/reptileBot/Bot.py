from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

# ??
import os
import re
import time
import codecs
import asyncio
import shutil
import configparser
config = configparser.ConfigParser() # ????

path = r'config.ini'
config.read(path)
api_id = config['base']['api_id']
api_hash = config['base']['api_hash']
bot_phone = config['base']['bot_phone']


if len(bot_phone) <=0:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), " | ", "未设置监听账号")
    os._exit(0)

print(time.strftime("%Y-%m-%d %H:%M:%S"),"api_id",api_id)
print(time.strftime("%Y-%m-%d %H:%M:%S"),"api_hash",api_hash)


def get_session():
    session_list = []
    for file in os.listdir("session"):
        file_name = str(file)
        if str(file_name).find('-journal') != -1:
            continue
        file_name = re.sub(".session", "", file_name)
        session_list.append(file_name)
    return session_list



async def client_init(session_string, api_id, api_hash):
    return TelegramClient('session/' + str(session_string), api_id, api_hash)


#
def errorHandling(s_string, error_e):
    log_string = str(error_e)
    if str(error_e).find("deleted/deactivated") != -1:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s_string, "] ????")

        log_string = log_string + "\n" + s_string + ":销号"

        shutil.copyfile("session/"+s_string+".session", "error-session/销号/" + s_string + ".session")
        if os.path.exists("session/"+s_string+".session") == True:
            os.remove("session/"+s_string+".session")


    fo = codecs.open("log/" + str(time.strftime("%Y-%m-%d")) + ".log", "a", 'utf-8')
    fo.write("\n\n=====================================================\n\n" + str(error_e))
    fo.close()


# ??????????????
async def detectJoin_FurChannel():
    session_list = get_session()
    for s in session_list:

        try:
            client_app = await client_init(s, api_id, api_hash)
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ????")
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ?????", str(e))
            continue


        try:
            await client_app.connect()
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ????")
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????", str(e))
            await client_app.disconnect()
            errorHandling(s, e)
            continue

        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ????????????")

        if str(is_private) == '1':
            try:
                channel_join = []
                async for dialog in client_app.iter_dialogs():
                    if dialog.is_channel == True:
                        channel_join.append(dialog.entity.id)
                        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ??????", dialog.entity.username)

            except Exception as e:
                await client_app.disconnect()
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ?????????", str(e))
                errorHandling(s, e)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ??????", str(e))
                continue

            try:
                await client_app(ImportChatInviteRequest(Fur_channel))
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ????????", Fur_channel)

                # print(e)
            except Exception as e:
                await client_app.disconnect()
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ????????12?", str(e))
                errorHandling(s, e)
                continue

            print(channel_join)
            await client_app.disconnect()
            continue




            # if Fur_channel not in channel_join:
            #     print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ??????", Fur_channel)
            #     print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????", Fur_channel)
            #     try:
            #         await client_app(JoinChannelRequest(Fur_channel))
            #         print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????", Fur_channel)
            #     except Exception as e:
            #         await client_app.disconnect()
            #         errorHandling(s, e)
            #         print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ????????", str(e))
            #         continue
            # else:
            #     print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????", Fur_channel)
        else:
            try:
                channel_join = []
                async for dialog in client_app.iter_dialogs():
                    if dialog.is_channel == True:
                        channel_join.append(dialog.entity.username)
                        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ??????", dialog.entity.username)

            except Exception as e:
                await client_app.disconnect()
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ?????????", str(e))
                errorHandling(s, e)
                continue

            if Fur_channel not in channel_join:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ??????",Fur_channel)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????",Fur_channel)
                try:
                    await client_app(JoinChannelRequest(Fur_channel))
                    print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????",Fur_channel)
                except Exception as e:
                    await client_app.disconnect()
                    errorHandling(s, e)
                    print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ????????", str(e))
                    continue
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????",Fur_channel)

        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????????")
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ???????????")

        await client_app.disconnect()
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "| [", s, "] ????")

async def main():
    await detectJoin_FurChannel()


asyncio.get_event_loop().run_until_complete(main())


