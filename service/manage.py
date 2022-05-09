#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import codecs
import json


def main():




    try:
        file_folder = [
            'session',
            'Message',
            'log',
            # 'log/client',
            'log/群发日志/',
            'log/加群日志/',
            'log/群发日志/client',
            'log/自动回复日志/',
            'log/自动回复日志/client',
            'Message/【私信广告词】',
            'Message/【群发广告词】',
            '91MBoss',
            '91MBoss/config',
            '91MBoss/error_log',
            '91MBoss/CronTab',
            '91MBoss/data',
            '91MBoss-session',
            '91MBoss-session/群发禁言',
            '91MBoss-session/加群帐号',
            '91MBoss-session/官方销号',
            '91MBoss-session/群发账号',

        ]
        for path in file_folder:
            if not os.path.exists(path):
                os.mkdir(path)

        file_list = [
            "91MBoss/config/channel_send.config.json",
        ]

        for file in file_list:
            if not os.path.exists(file):
                file = open(file, 'w')
                file.close()

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc



    try:
        path = "91MBoss/config/channel_send.config.json"
        f = open(path, encoding="utf-8")
        content = f.read()
        f.close()

        if content == '':

            content = {
                "client_number":'',
                "sleep_time":'8',
                "is_fake_content":'2',
                "fake_content_sleep_time":'2',
                "StartGroupSendTask":'2',#启动群发任务
                "StartGroupJoinTask": '2',  # 启动加群任务
                "StartPrivateLetterTask":'2',#启动私信任务
                "StartPrivateLetterBombingTask":'2',#启动私信轰炸任务
                "automaticReply":'',#自动回复
            }
            fo = codecs.open(path, "a", 'utf-8')
            fo.write(json.dumps(content))
            fo.close()

    except Exception as e:

        print(str(e))














    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
