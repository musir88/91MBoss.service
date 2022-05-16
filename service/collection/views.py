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


def collection_channelUser(request):
    print("collection_channelUser")

    context = {
        'latest_question_list': 'opio',

    }
    return render(request, 'collection/collection_channelUser.html', {'context': context})