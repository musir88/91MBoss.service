from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import os
import time
import json
import codecs

admin_host = "http://91m.live/clientlogin"

class AUTH91MBoss(MiddlewareMixin):
    def process_request(self, request):
        # print("md1  process_request 方法。", id(request))  # 在视图之前执行

        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH')

        # client_number
        i=1
        if 1==i:
            # print(request.path_info)

            if "/number_list/client_number" != request.path_info:

                path = "91MBoss/config/auth-session.json"
                if not os.path.exists(path):
                    if is_ajax == 'XMLHttpRequest':
                        return HttpResponse(json.dumps({
                            'status':False,
                            'status':"登录失效，请前往 主页 重新登录",
                        }, ensure_ascii=False))
                    return redirect('client_number')

                auth_session = request.session.get("auth-sesion", None)
                if auth_session == None:

                    f = open(path, encoding="utf-8")
                    client_param = f.read()
                    client_param = json.loads(client_param)
                    client_param['submit_code'] = "AUTH91MBoss"
                    client_param['ip'] = self.get_request_ip(request)
                    f.close()

                    admin_host = "http://91m.live/clientlogin"
                    res = requests.post(url=admin_host, data=client_param, verify=False)

                    try:
                        response = json.loads(res.text)
                        # print(time.strftime("%Y-%m-%d %H:%M:%S"), "|",response['message'])
                    except Exception as e:
                        print(time.strftime("%Y-%m-%d %H:%M:%S"), "|",str(e))
                    # print(response)


                    # return ''

                    # if response['status'] == False:
                    #     request.session['client_number_message'] = response['message']
                    #     if is_ajax == 'XMLHttpRequest':
                    #         return HttpResponse(json.dumps(response, ensure_ascii=False))
                    #     return redirect('client_number')
                    #
                    # if response['status'] == True:
                    #     request.session['auth-sesion'] = response
                    #     request.session.set_expiry(600)

    def get_request_ip(self, request):
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip




    pass