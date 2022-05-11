from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
import requests
import os
import json
import codecs

admin_host = "http://91m.live/clientlogin"

class AUTH91MBoss(MiddlewareMixin):
    def process_request(self, request):
        print("md1  process_request 方法。", id(request))  # 在视图之前执行




        # client_number
        if "/number_list/client_number" != request.path_info:

            path = "91MBoss/config/auth-session.json"
            if not os.path.exists(path):
                return redirect('client_number')

            auth_session = request.session.get("auth-sesion", None)
            if auth_session == None:

                f = open(path, encoding="utf-8")
                client_param = f.read()
                client_param = json.loads(client_param)
                f.close()

                admin_host = "http://91m.live/clientlogin"
                res = requests.post(url=admin_host, data=client_param, verify=False)
                response = json.loads(res.text)

                if response['status'] == False:
                    return redirect('client_number')

                if response['status'] == True:
                    request.session['auth-sesion'] = response
                    request.session.set_expiry(7200)


    pass