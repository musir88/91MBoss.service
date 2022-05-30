from django.shortcuts import render
from pathlib import Path
import os
import json
import codecs
import os
import re
import time
import random
from datetime import date, timedelta
import requests
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
import base64



headers={
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
  "Connection":"keep-alive",
  "Host":  "36kr.com/newsflashes",
  "Upgrade-Insecure-Requests":"1",
  "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"
}

ua_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
]






def client_init(result):
    proxy_param = proxy_set()

    proxy_param = ''
    if 'proxy' in result:
        proxy_param = result['proxy']
    else:
        proxy_path = "91MBoss/config/proxy.json"
        if os.path.exists(proxy_path) == True:
            # proxy_all = get_config(proxy_path)
            # if len(proxy_all) <1:
            #     proxy_param = ''
            # else:
            #     proxy_param = proxy_all.pop()
            #     if len(proxy_all) < 1:
            #         proxy_all = []
            #     set_config(proxy_path, proxy_all)


            admin_host = "http://api.proxy.ipidea.io/getProxyIp"
            # "http://api.proxy.ipidea.io/getProxyIp?num=1&return_type=json&lb=1&sb=0&flow=1&regions=vn&protocol=socks5"
            res = requests.post(url=admin_host, data={
                "num":1,
                "return_type":'json',
                "regions":'vn',
                # "regions":'us',
                "protocol":'socks5',
                "flow":1,
                "lb":1,
                "sb":0,
            }, verify=False)
            pro_response = json.loads(res.text)
            print(pro_response)
            if pro_response['success'] == True:
                print(pro_response['data'])
                proxy_param = {
                    'host': pro_response['data'][0]['ip'],
                    'port': pro_response['data'][0]['port'],
                    'username': '',
                    'password': ''
                }
            else:
                proxy_param = ''


        else:
            proxy_param = ''




    # proxy = (socks.SOCKS5, "'216.185.46.23", "49161", 'tigerfpv', "V4LEgUcmy7")
    # proxy = (socks.SOCKS5, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])








    # print("client_init:"+str(proxy_param))
    # config = {}
    # config['proxy'] = proxy
    # config['api'] = {
    #     'api_id':int(result['api_id']),
    #     'api_hash':str(result['api_hash']),
    # }
    path = "91MBoss/config/api/"+ str(result['phone']) +".json"
    if os.path.exists(path) == True:
        os.remove(path)

    fo = codecs.open(path, "a", 'utf-8')
    fo.write(json.dumps({
        "api_id":int(result['api_id']),
        "api_hash":str(result['api_hash']),
        "proxy":proxy_param
    }))
    fo.close()

    path = "91MBoss-session/自动注册"
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists("91MBoss-session/自动注册/注册成功"):
        os.mkdir("91MBoss-session/自动注册/注册成功")

    # if proxy_param == '':
    if proxy_param != '':
        print('==================================')
        return TelegramClient(
            path + '/' + str(result['phone']),
            int(result['api_id']),
            str(result['api_hash'])
        )
    else:

        print(socks.SOCKS5)
        # proxy = (
        #     int(socks.SOCKS5),
        #     str(proxy_param['host']),
        #     str(proxy_param['port']),
        #     # str(proxy_param['username']),
        #     'user name',
        #     str(proxy_param['password'])
        # )
        # proxy = {
        #     'proxy_type': 'SOCKS5',  # (mandatory) protocol to use (see above)
        #     'addr': str(proxy_param['host']),  # (mandatory) proxy IP address
        #     'port': int(proxy_param['port']),  # (mandatory) proxy port number
        #     'username': 'Administrator',  # (optional) username if the proxy requires auth
        #     # 'username': str(proxy_param['username']),  # (optional) username if the proxy requires auth
        #     'password': str(proxy_param['password']),  # (optional) password if the proxy requires auth
        #     'rdns': True  # (optional) whether to use remote or local resolve, default remote
        # }
        # {'host': '216.185.47.218', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'}

        # proxy = {
        #     'proxy_type': 'SOCKS5',  # (mandatory) protocol to use (see above)
        #     'addr': str('216.185.47.218'),  # (mandatory) proxy IP address
        #     'port': int('49161'),  # (mandatory) proxy port number
        #     'username': 'tigerfpv',  # (optional) username if the proxy requires auth
        #     # 'username': str(proxy_param['username']),  # (optional) username if the proxy requires auth
        #     'password': str('V4LEgUcmy7'),  # (optional) password if the proxy requires auth
        #     'rdns': True  # (optional) whether to use remote or local resolve, default remote
        # }

        # proxy = (socks.SOCKS5, str('52.28.250.157'), int('40000'), 'user name', 'cf1cb611')
        # proxy = (socks.SOCKS5, str('216.185.47.218'), int('49161'), 'tigerfpv', 'V4LEgUcmy7')
        print('==================================')
        print('==================================')
        # proxy = (socks.SOCKS5, str('50.114.107.228'), int('49161'), 'tigerfpv', 'V4LEgUcmy7')
        # proxy = (socks.SOCKS5, str('50.114.107.223'), int('49161'), 'tigerfpv', 'V4LEgUcmy7')
        # proxy = (socks.SOCKS5, str('13.229.197.225'), int('40000'), 'user name', 'bbda6b92')
        # proxy = (socks.SOCKS5, str('18.139.39.145'), int('40000'), 'user name', '13a164bf')
        # proxy = (socks.SOCKS5, str('54.83.81.113'), int('11446'), '', '') str(proxy_param['username'])
        proxy = (socks.SOCKS5, str(proxy_param['host']), int(proxy_param['port']), str(proxy_param['username']), str(proxy_param['password']))

        print('==================================')
        print('==================================')
        print('==================================')
        print('==================================')
        print('==================================')
        print('==================================')

        return TelegramClient(
            path+'/' + str(result['phone']),
            int(result['api_id']),
            str(result['api_hash']),
            proxy=proxy
        )


def proxy_set():
    proxy = [
        {'host': '216.185.47.218', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.228', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.105', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.220', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '154.16.150.211', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.226', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.104', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.23', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.223', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.28', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
    ]
    return random.choice(proxy)


def api_idhash(request=None):
    proxy = [
        {'api_id': 18806282, 'api_hash': 'cbfa09dd409ad53fba7ebce2ad477'},
        {'api_id': 15718961, 'api_hash': '6355e6f68264228fbf0bff8891ad0370'},
        {'api_id': 17345465, 'api_hash': '1fcfcffb77d010b5235b13e840a158ef'},
        {'api_id': 12971859, 'api_hash': '2f5003c9d36f74d32bbd252391a386f8'},
        {'api_id': 14545894, 'api_hash': '6d3d71e021a42cfe83f03c888f7a8c28'},
        {'api_id': 12564222, 'api_hash': 'e5f301c0c350c9a49b7adac287c3100f'},
        {'api_id': 13869498, 'api_hash': '3bb10d91b3b12994f3de37839fa98a3b'},
        {'api_id': 14849339, 'api_hash': '371ec4e9d10e482035d177cd2c55056e'},
        {'api_id': 15579305, 'api_hash': '5b139aeb5136fb5d794e9a3eb02d9397'},
    ]

    path = "91MBoss/config/api_config/"
    list = []
    for file in os.listdir(path):
        file_name = str(file)
        list.append(file_name)

    if len(list) < 1:
        return {
            "status": False,
            "message": "没有设置开发号",
            'api': ''
        }

    if request == None:
        random.shuffle(list)
        content = list.pop()
    else:
        sup_api_id = request.session.get("sup_api_id", None)
        id_key = 0
        if sup_api_id != None:
            if len(list) >= int(sup_api_id):
                id_key = sup_api_id
            else:
                id_key = 0
        content = list.pop(id_key)
        request.session.get("sup_api_id", int(id_key)+1)



    f = open(path + content, encoding="utf-8")
    content = f.read()
    content = json.loads(content)
    f.close()
    return {
        'status':True,
        'api':content
    }



def sms_man_rejectActivation(result):
    respose = result['api_respose'].split(":")
    # print(respose)
    # print(respose[1])
    api = "http://api.sms-man.com/stubs/handler_api.php"

    config = get_config("91MBoss/config/sup.smsman.json")
    api_param = {
        "action":"setStatus",
        "api_key":config['SecretKey'],
        "id":respose[1],
        "status":-1,
    }
    respose = requests.post(url=api, data=api_param, verify=False)
    respose = respose.text
    return respose



def error_response(result):
    result['submit_code'] = ''

    if str(result['message']).find("The used phone number has been banned from Telegram and cannot be used anymore") != -1 :
        result['submit_code'] = "close"
        result['message'] = "官方禁用 " + str(result['message'])

    if str(result['message']).find("A wait of") != -1:
        result['submit_code'] = "close"
        result['message'] = "开发号频繁 " + str(result['message'])

    if str(result['message']).find("Two-steps verification is enabled and a password is required") != -1:
        result['submit_code'] = "close"
        result['message'] = "启用两步验证，需要密码（由SignInRequest引起）" + str(result['message'])


    if str(result['message']).find("未出码") != -1:
        result['submit_code'] = "close"


    if result['submit_code'] == "close":
        if result['api_code'] == "sms-man":
            rejectActivation_respose = sms_man_rejectActivation(result)
            result['rejectActivation_respose'] = str(rejectActivation_respose)





    string = "【 "+str(time.strftime("%Y-%m-%d %H:%M:%S"))+" 】"
    for item in result:
        string = str(string) + "\n"+str(item)+" → " + str(result[item])



    fo = codecs.open("91MBoss/error_log/sup" + str(date.today()) + ".log", "a", 'utf-8')
    fo.write("\n\n=============================================\n\n" + str(string))
    fo.close()

    return result


def get_config(path):
    if os.path.exists(path) ==True:
        f = open(path, encoding="utf-8")
        content = f.read()
        f.close()
        # return content
        return json.loads(content)
    else:
        return {}

def set_config(path, content):
    if os.path.exists(path) ==True:
        os.remove(path)
    fo = codecs.open(path, "a", 'utf-8')
    fo.write(json.dumps(content))
    fo.close()
    return True

async def sup_smsmain(request):
    result = {
        "api_id":"18806282",
        "api_hash":"943cbfa09dd409ad53fba7ebce2ad477",
    }

    idhash = api_idhash(request)
    result = idhash['api']
    if idhash['status'] == False and request.method == 'GET':
        result['status'] = False
        context = {}
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    result['api_code'] = 'sms-man'

    if request.method == 'GET':
        data = request.GET
        api_data = {
            'phone': data['phone'],
            'api_respose': data['api_respose'],
            'sup_step': '1',
        }

    if request.method == 'POST':
        data = request.POST
        api_data = {
            'phone': data['phone'],
            'api_respose': data['api_respose'],
            'sup_step': '2',
            'code': data['code'],
            'phone_code_hash': data['phone_code_hash']
        }

        if 'proxy_host' in data:
            result['proxy'] = {
                'host':data['host'],
                'port':data['port'],
                'username':data['username'],
                'password':data['password']
            }



        result['phone_code_hash'] = api_data['phone_code_hash']
        # print(api_data)

        if "api_hash" in data:
            result['api_hash'] = data['api_hash']

        if "api_id" in data:
            result['api_id'] = data['api_id']


    context = {
        "api_data": api_data,
    }

    result['phone'] = api_data['phone']
    result['api_respose'] = api_data['api_respose']





    try:
        client = client_init(result)
    except Exception as e:
        result['status'] = False
        result['message'] = "client_init:"+str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    api_path = "91MBoss/config/api/" + str(result['phone']) + ".json"
    if os.path.exists(api_path) == True:
        api_config_s = get_config(api_path)
        if 'proxy' in api_config_s:
            result['proxy'] = api_config_s['proxy']


    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result['status'] = False
        result['message'] =  "connect:"+str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    if str(api_data['sup_step']) == '1':
        try:
            sent = await client.send_code_request(result['phone'], force_sms=True)
            # print('===================================================')
            # print(sent)
            phone_code_hash = sent.phone_code_hash
            result['status'] = True
            result['phone_code_hash'] = phone_code_hash
            result['message'] = '发送验证码成功'
            context['result'] = result
            await client.disconnect()
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result = error_response(result)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

    if str(api_data['sup_step']) == '2':

        try:
            first_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(7, 13)))
            last_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(8, 15)))

            await client.sign_up(
                code=api_data['code'],
                first_name=first_name,
                last_name=last_name,
                phone=result['phone'],
                phone_code_hash=api_data['phone_code_hash']
            )
            result['phone_code_hash'] = api_data['phone_code_hash']
            shutil.copyfile("91MBoss-session/自动注册/" + result['phone'] + ".session", "91MBoss-session/自动注册/注册成功/" + result['phone'] + ".session")
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result = error_response(result)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})


        # 设置二次验证码
        try:
            await client.edit_2fa(new_password='91m123456')
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

        # 设置用户名
        try:
            username = "boss"+''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(6, 12)))
            await client(UpdateUsernameRequest(username))
            result['username'] = username
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})

        await client.disconnect()
        result['status'] = True
        result['message'] = "SUP-成功"
        result['submit_code'] = "close"
        context['result'] = result
        return render(request, 'AutomaticSup/sup_smsmain.html', {"context": context})





from urllib.parse import urlparse
def sms_man(request):
    # response = requests.get(str(resolve('/user/addContacts').route)+"?phone=919923144199&contacts_numbere=919923144190",verify=False)
    # print(response)

    path = "91MBoss/config/sup.smsman.json"
    if request.method == 'POST':
        data = request.POST
        config = {
            'SecretKey': data['SecretKey'],
            'nation': data['nation']
        }
        set_config(path, config)
        return redirect('automaticSupSms_man')

    context = {
        "config":get_config(path)
    }

    return render(request, 'AutomaticSup/sms_man.html', {"context":context})



def get_smsmainNumber(request):

    config = get_config("91MBoss/config/sup.smsman.json")
    country_list = config['nation'].split(",")

    random.shuffle(country_list)
    country = country_list.pop()
    SecretKey = config['SecretKey']

    api = "https://api.sms-man.com/stubs/handler_api.php"
    api_param = {
        "ref":"xRMGluESoodc",
        "country":country,
        "service":"tg",
        "action":"getNumber",
        "api_key":SecretKey
    }

    respose = requests.post(url=api, data=api_param, verify=False)
    respose = respose.text

    if respose.find("ACCESS_NUMBER") != -1:
        result = respose.split(":")
        # print(result[2])
        # addContacts

        next = request.META.get('HTTP_REFERER', None) or '/'
        urlp = urlparse(next)

        addContactsApi = str(urlp.scheme) + "://" + str(urlp.netloc) + "/user/addContacts?phone=919923144199&contacts_numbere="+str(result[2])
        print(addContactsApi)
        response = requests.get(addContactsApi, verify=False)
        response = json.loads(response.text)
        print(response)
        if response['status'] == True:
            sms_man_rejectActivation({"api_respose":respose})

            return HttpResponse(json.dumps({
                "status": False,
                "message": "该账号已经被注册过:" + str(respose),
            }, ensure_ascii=False))







        return HttpResponse(json.dumps({
            "status": True,
            "phone": result[2],
            "api_respose": respose,
            "message": str(country)+"账号:" + str(respose) ,
        }, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "没有账号:" + str(respose),
        }, ensure_ascii=False))


def sup_smsmain_getcode(request):
    data = request.POST
    timing = data['timing']
    api_respose = data['api_respose']

    if int(timing) >400:
        result = error_response({
            'api_code':"sms-man",
            'api_respose':str(api_respose),
            'message':str(api_respose)+" 取码400次未出码主动放弃",
        })

        return HttpResponse(json.dumps({
            "status": False,
            "submit_code": "close",
            "message": str(data['api_respose']) + " → " + str(result['message']),
        }, ensure_ascii=False))


    api_respose = api_respose.split(":")
    api_id = api_respose[1]

    config = get_config("91MBoss/config/sup.smsman.json")
    country_list = config['nation'].split(",")
    SecretKey = config['SecretKey']

    api = "https://api.sms-man.com/stubs/handler_api.php"
    api_param = {
        "id": api_id,
        "action": "getStatus",
        "api_key": SecretKey
    }
    respose = requests.post(url=api, data=api_param, verify=False)
    respose = respose.text

    if 'STATUS_CANCEL' == str(respose):

        result = error_response({
            'api_code':"sms-man",
            'api_respose':str(api_respose),
            'message':str(respose),
        })

        return HttpResponse(json.dumps({
            "status": False,
            "submit_code": "close",
            "message": str(data['api_respose'])+" 超时："+str(respose),
        }, ensure_ascii=False))

    if str(respose).find("STATUS_OK") != -1:
        result = respose.split(":")
        # print(result)
        return HttpResponse(json.dumps({
            "status": True,
            "message": str(data['api_respose']) + " ==> " + str(respose),
            "code": str(result[1]),
        }, ensure_ascii=False))

    return HttpResponse(json.dumps({
        "status": False,
        "message": str(data['api_respose'])+" 没有获取到: " + str(respose),
    }, ensure_ascii=False))

def automaticSup_api1(request):
    path = "91MBoss/config/sup.automaticSup_api1.json"

    if request.method == 'POST':
        api_string = request.POST['api']
        area_code = request.POST['area_code']
        api = []
        for i in api_string.split("\n"):
            i = i.replace("\r",'')
            if len(i) < 1:
                continue
            i = str(area_code)+str(i)
            api.append(i)

        set_config(path, api)
        return redirect('automaticSup_api1')


    string = ""
    context = get_config(path)
    for c in context:
        string = string +"\n" + c

    return render(request, 'AutomaticSup/automaticSup_api1.html', {"context": string})


def get_automaticSup_api1Number(request):
    path = "91MBoss/config/sup.automaticSup_api1.json"
    string = ""
    context = get_config(path)
    for c in context:
        string = string +"\n" + c
    string = string.strip()

    if len(context) < 1:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "没有号了 如果要上号一定要刷新页面之后再操作",
            "context": string,
        }, ensure_ascii=False))

    number_ = context.pop(0)

    if len(number_) < 1:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "没有号了 如果要上号一定要刷新页面之后再操作",
            "context": string,
        }, ensure_ascii=False))
    number = number_.split("\t")

    api = {
        "phone":str(number[0]),
        "api_respose":str(number[1]),
    }
    # print(api)
    if len(context) <1:
        context = []
    set_config(path, context)

    s = str(api['api_respose'])
    s = base64.b64encode(s.encode())
    s = str(s)
    s = s.replace("b'","")
    s = s.replace("'","")

    return HttpResponse(json.dumps({
        "status": True,
        "api": api,
        "phone": api['phone'],
        "api_respose": str(s),
        "message": "账号:" + str(number_) + "\t" + str(api['api_respose']),
        "context": string,

    }, ensure_ascii=False))



async def sup_automaticSup_api(request):

    idhash = api_idhash()
    result = idhash['api']
    result['api_id'] = int(result['api_id'])
    if idhash['status'] == False and request.method == 'GET':
        result['status'] = False
        context = {}
        context['result'] = result
        return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})

    result['api_code'] = 'api-1'

    if request.method == 'GET':
        data = request.GET
        api_data = {
            'phone': data['phone'],
            'api_respose': data['api_respose'],
            'sup_step': '1',
        }

    if request.method == 'POST':
        data = request.POST
        api_data = {
            'phone': data['phone'],
            'api_respose': data['api_respose'],
            'sup_step': '2',
            'code': data['code'],
            'phone_code_hash': data['phone_code_hash']
        }

        if 'proxy_host' in data:
            result['proxy'] = {
                'host':data['host'],
                'port':data['port'],
                'username':data['username'],
                'password':data['password']
            }

        result['phone_code_hash'] = api_data['phone_code_hash']
        # print(api_data)

        if "api_hash" in data:
            result['api_hash'] = data['api_hash']

        if "api_id" in data:
            result['api_id'] = data['api_id']


    context = {
        "api_data": api_data,
    }

    result['phone'] = str(api_data['phone'])
    result['api_respose'] = api_data['api_respose']



    try:
        print(result)
        client = client_init(result)
    except Exception as e:
        result['message'] = str(e)
        result['status'] = False
        result = error_response(result)
        # 号给加回去
        s = base64.b64decode(result['api_respose']).decode()
        s = str(s)
        path_ = "91MBoss/config/sup.automaticSup_api1.json"
        number_string = str(result['phone']) + "\t" + s
        number_string = str(number_string)
        c = get_config(path_)
        c.append(number_string)
        set_config(path_, c)

        result['status'] = False
        result['message'] = "client_init:"+str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})

    api_path = "91MBoss/config/api/" + str(result['phone']) + ".json"
    if os.path.exists(api_path) == True:
        api_config_s = get_config(api_path)
        if 'proxy' in api_config_s:
            result['proxy'] = api_config_s['proxy']
            print(result)




    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()

        # 号给加回去
        # s = base64.b64decode(result['api_respose']).decode()
        # s = str(s)
        # path_ = "91MBoss/config/sup.automaticSup_api1.json"
        # number_string = str(result['phone']) + "\t" + s
        # number_string = str(number_string)
        # c = get_config(path_)
        # c.append(number_string)
        # set_config(path_, c)

        # result = error_response(result)
        result['status'] = False
        result['message'] =  "connect:"+str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})

    if str(api_data['sup_step']) == '1':
        try:
            # sent = await client.send_code_request(result['phone'], force_sms=True)
            sent = await client.send_code_request(result['phone'])
            # print('===================================================')
            # print(sent)
            phone_code_hash = sent.phone_code_hash
            result['status'] = True
            result['phone_code_hash'] = phone_code_hash
            result['message'] = '发送验证码成功'
            context['result'] = result
            await client.disconnect()
            return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result = error_response(result)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})

    if str(api_data['sup_step']) == '2':

        try:
            first_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(7, 13)))
            last_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(8, 15)))

            await client.sign_up(
                code=api_data['code'],
                first_name=first_name,
                last_name=last_name,
                phone=result['phone'],
                phone_code_hash=api_data['phone_code_hash']
            )
            result['phone_code_hash'] = api_data['phone_code_hash']
            shutil.copyfile("91MBoss-session/自动注册/" + result['phone'] + ".session", "91MBoss-session/自动注册/注册成功/" + result['phone'] + ".session")
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result = error_response(result)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})


        # 设置二次验证码
        try:
            await client.edit_2fa(new_password='91m123456')
        except Exception as e:
            await client.disconnect()
            result = error_response(result)
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})

        # 设置用户名
        try:
            username = "boss"+''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(6, 12)))
            await client(UpdateUsernameRequest(username))
            result['username'] = username
        except Exception as e:
            await client.disconnect()
            result = error_response(result)
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})

        await client.disconnect()
        result['status'] = True
        result['message'] = "SUP-注册-成功"
        result['submit_code'] = "close"
        context['result'] = result
        return render(request, 'AutomaticSup/sup_automaticSup_api.html', {"context": context})

def sup_automaticSup_api_getcode(request):
    data = request.POST
    timing = data['timing']
    api_respose = data['api_respose']

    if int(timing) >400:
        result = error_response({
            'api_code':"api-1",
            'api_respose':str(api_respose),
            'message':str(api_respose)+" 取码400次未出码主动放弃",
        })

        return HttpResponse(json.dumps({
            "status": False,
            "submit_code": "close",
            "message": str(data['api_respose']) + " → " + str(result['message']),
        }, ensure_ascii=False))

    api_respose = base64.b64decode(api_respose).decode()




    respose = requests.get(url=api_respose, verify=False)
    # respose = requests.post(url=api_respose, data={}, verify=False)
    respose = respose.text
    # print('=======================')
    # print(api_respose)
    # print(str(respose))
    # print('=======================')

    if str(respose).find('暂未登录或token已经过期') != -1:
        result = error_response({
            'api_code':"api-1",
            'api_respose':str(api_respose),
            # "submit_code": "close",
            'message':str(respose),
        })
        return HttpResponse(json.dumps({
            "status": False,
            # "submit_code": "close",
            "message": str(data['api_respose']) + " →2 " + str(respose),
        }, ensure_ascii=False))
    # print('=======================')

    # respose = "Telegram code 29065"
    # print(respose)
    if str(respose).find("Telegram code") != -1:
        if str(respose).find("https://t.me/login/") != -1:
            result = respose.split("https://t.me/login/")[1]
        else:
            result = respose.split("Telegram code")[1]
        result = result.strip()
        # print('===============================================')

        return HttpResponse(json.dumps({
            # "status": False,
            "status": True,
            "message": str(data['api_respose']) + " ==> " + str(respose),
            "code": str(result),
        }, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "message": str(data['api_respose'])+" 未获取到验证码："+str(respose),
        }, ensure_ascii=False))


def automaticSup_ahasim(request):
    path = "91MBoss/config/sup.ahasim.json"
    if request.method == 'POST':
        data = request.POST
        config = {
            'SecretKey': data['SecretKey']
        }
        set_config(path, config)
        return redirect('automaticSup_ahasim')

    context = {
        "config":get_config(path)
    }

    return render(request, 'AutomaticSup/automaticSup_ahasim.html', {"context":context})

def get_supNumber(request):





    if request.method == 'POST':
        req_data = request.POST
        if "action_token" not in req_data:
            return HttpResponse(json.dumps({
                "status": False,
                "message": "ACTION_TOKEN1",
            }, ensure_ascii=False))

        action_token = req_data['action_token']
        if str(action_token) == 'ahasim.com':
            path = "91MBoss/config/sup.ahasim.json"
            config = get_config(path)
            if config['SecretKey'] == '' or 'SecretKey' not in config:
                return HttpResponse(json.dumps({
                    "status": False,
                    "message": "请设置秘钥",
                }, ensure_ascii=False))

            api_host = "http://ahasim.com/api/phone/new-session?token="+config['SecretKey']+"&service=5"
            res = requests.get(api_host,headers={'User-Agent': random.choice(ua_list)}, verify=False)
            # res = requests.post(url=api_host, data={
            #     "token": config['SecretKey'],
            #     "service": 5,
            # }, verify=False)
            response = json.loads(res.text)
            # print(pro_response)
            print(response)

            if response['success'] == False:
                return HttpResponse(json.dumps({
                    "status": False,
                    "response": response,
                    "message": response['message'],
                }, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({
                    "status": True,
                    "response": response,
                    "phone": "84"+str(response['data']['phone_number']),
                    "api_respose": response['data']['session'],
                    "message": "84"+str(response['data']['phone_number']) +' ok',
                }, ensure_ascii=False))


        return HttpResponse(json.dumps({
            "status": False,
            "message": "ACTION_TOKEN2",
        }, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "访问错误",
        }, ensure_ascii=False))

async def sup_ahasim(request):
    result = {
        "api_id": "18806282",
        "api_hash": "943cbfa09dd409ad53fba7ebce2ad477",
    }

    idhash = api_idhash()
    result = idhash['api']
    if idhash['status'] == False and request.method == 'GET':
        result['status'] = False
        context = {}
        context['result'] = result
        return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})

    result['api_code'] = 'ahasim'

    if request.method == 'GET':
        data = request.GET
        api_data = {
            'phone': data['phone'],
            'api_respose': data['api_respose'],
            'sup_step': '1',
        }

    if request.method == 'POST':
        data = request.POST
        api_data = {
            'phone': data['phone'],
            'api_respose': data['api_respose'],
            'sup_step': '2',
            'code': data['code'],
            'phone_code_hash': data['phone_code_hash']
        }

        if 'proxy_host' in data:
            result['proxy'] = {
                'host': data['host'],
                'port': data['port'],
                'username': data['username'],
                'password': data['password']
            }

        result['phone_code_hash'] = api_data['phone_code_hash']
        # print(api_data)

        if "api_hash" in data:
            result['api_hash'] = data['api_hash']

        if "api_id" in data:
            result['api_id'] = data['api_id']

    context = {
        "api_data": api_data,
    }

    result['phone'] = api_data['phone']
    result['api_respose'] = api_data['api_respose']

    try:
        client = client_init(result)
    except Exception as e:
        result['status'] = False
        result['message'] = "client_init:" + str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})

    api_path = "91MBoss/config/api/" + str(result['phone']) + ".json"
    if os.path.exists(api_path) == True:
        api_config_s = get_config(api_path)
        if 'proxy' in api_config_s:
            result['proxy'] = api_config_s['proxy']

    try:
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result['status'] = False
        result['message'] = "connect:" + str(e)
        context['result'] = result
        return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})

    if str(api_data['sup_step']) == '1':
        try:
            sent = await client.send_code_request(result['phone'])
            # sent = await client.send_code_request(result['phone'], force_sms=True)
            # print('===================================================')
            # print(sent)
            phone_code_hash = sent.phone_code_hash
            result['status'] = True
            result['phone_code_hash'] = phone_code_hash
            result['message'] = '发送验证码成功'
            context['result'] = result
            await client.disconnect()
            return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result = error_response(result)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})

    if str(api_data['sup_step']) == '2':

        try:
            first_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(7, 13)))
            last_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(8, 15)))

            await client.sign_up(
                code=api_data['code'],
                first_name=first_name,
                last_name=last_name,
                phone=result['phone'],
                phone_code_hash=api_data['phone_code_hash']
            )
            result['phone_code_hash'] = api_data['phone_code_hash']
            shutil.copyfile("91MBoss-session/自动注册/" + result['phone'] + ".session",
                            "91MBoss-session/自动注册/注册成功/" + result['phone'] + ".session")
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result = error_response(result)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})

        # 设置二次验证码
        try:
            await client.edit_2fa(new_password='91m123456')
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})

        # 设置用户名
        try:
            username = "boss" + ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], random.randint(6, 12)))
            await client(UpdateUsernameRequest(username))
            result['username'] = username
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            context['result'] = result
            return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})

        await client.disconnect()
        result['status'] = True
        result['message'] = "SUP-成功"
        result['submit_code'] = "close"
        context['result'] = result
        return render(request, 'AutomaticSup/sup_ahasim.html', {"context": context})

def sup_ahasim_getcode(request):
    data = request.POST
    timing = data['timing']
    api_respose = data['api_respose']

    if int(timing) > 400:
        result = error_response({
            'api_code': "ahasim",
            'api_respose': str(api_respose),
            'message': str(api_respose) + " 取码400次未出码主动放弃",
        })

        return HttpResponse(json.dumps({
            "status": False,
            "submit_code": "close",
            "message": str(data['api_respose']) + " → " + str(result['message']),
        }, ensure_ascii=False))

    # api_respose = base64.b64decode(api_respose).decode()

    path = "91MBoss/config/sup.ahasim.json"
    config = get_config(path)
    if config['SecretKey'] == '' or 'SecretKey' not in config:
        return HttpResponse(json.dumps({
            "status": False,
            "message": "请设置秘钥",
        }, ensure_ascii=False))

    api_host = "http://ahasim.com/api/session/" + api_respose + "/get-otp?token=" + config['SecretKey']
    respose = requests.get(api_host, headers={'User-Agent': random.choice(ua_list)}, verify=False)
    respose = json.loads(respose.text)
    print('=======================')
    # print(api_respose)
    print(respose)
    print('=======================')

    return HttpResponse(json.dumps({
        "status": False,
        "respose": respose,
        "message": " 未获取到验证码：" + str(respose),
    }, ensure_ascii=False))


    # respose = "Telegram code 29065"
    # print(respose)
    if str(respose).find("Telegram code") != -1:
        if str(respose).find("https://t.me/login/") != -1:
            result = respose.split("https://t.me/login/")[1]
        else:
            result = respose.split("Telegram code")[1]
        result = result.strip()
        # print('===============================================')

        return HttpResponse(json.dumps({
            # "status": False,
            "status": True,
            "message": str(data['api_respose']) + " ==> " + str(respose),
            "code": str(result),
        }, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "message": str(data['api_respose']) + " 未获取到验证码：" + str(respose),
        }, ensure_ascii=False))