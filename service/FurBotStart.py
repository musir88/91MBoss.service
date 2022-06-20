import os
import requests
import socket
import json
import time
import configparser
config = configparser.ConfigParser() # 类实例化

path = r'Fur_config.ini'
config.read(path)
number = config['user']['number']

print(socket.gethostname())

admin_host = "http://91m.live/clientlogin"
res = requests.post(url=admin_host, data={
    'client_number':number,
    'submit_code':"client_number",
    "ip":socket.gethostbyname(socket.gethostname()),
    "os_name":socket.gethostname()
}, verify=False)

try:
    response = json.loads(res.text)
    # print(time.strftime("%Y-%m-%d %H:%M:%S"), "|",response['message'])
except Exception as e:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "|", str(e))

if response['status'] == False:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "|", response['message'])
    os._exit(0)
    input("回车退出软件")
else:
    os.system('1.exe && 2.exe')