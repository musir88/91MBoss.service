import requests

response = requests.post(url="http://127.0.0.1:8910/collection/collection_channelUser_submit", data={
    # 'CHANNEL':'bs91m990',
    'CHANNEL':'https://t.me/sichouzhilu0',
    'TIME_FILTER_DAYS':1,
    'IS_SPECIFY_GROUP':1,
    'IS_FILTER_PHOTO':1,
    'ID_FILTER_LEN':5,
}, verify=False)

print(response.text)


