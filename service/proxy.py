import requests
import json

admin_host = "http://api.proxy.ipidea.io/getProxyIp"

res = requests.post(url=admin_host, data={
    "num": 1,
    "return_type": 'json',
    "regions": 'us',
    "protocol": 'socks5',
    "flow": 1,
    "lb": 1,
    "sb": 0,
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


print(proxy_param)
