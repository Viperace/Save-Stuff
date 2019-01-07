
# -*- coding: utf-8 -*-
import multiprocessing
import os, sys, re, socks, time, platform, shutil, random, math
import string

from telethon import TelegramClient, sync, errors
from telethon.errors import SessionPasswordNeededError
from telethon.tl.custom import Button
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest, EditBannedRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, ChannelBannedRights, InputMessagesFilterPhotos
# from tasks import CeleryInviteUser



testinfo = {
# 申请api接口
# https://my.telegram.org/apps
#电话号码,电话号码,api ,key
    '17130604752': ('1713060475?', 0000000, 'Xd3d13319472fd1ed0a6db24a22c2a28'),
d73f90d14f8a78531845692ec93f7562

}


def getrun(value):
    # +86这里我是填中国你可以填新加坡的
    print('+86' + str(value[0]))
    print('>>>>loading...')
    try:

        client = TelegramClient(*value)

        print('>>>>ok...')
        if not client.is_user_authorized():
            print('>>>> client  not !')
            raise
        #核心代码就是这个位置.你可以用这个方法去接收任意群的消息 我用的是同步方法.有异步方法.我不会用.
        #这里可以获取群或用户发给你的数据这里的意思是 只接收最后10条
        for message in client.iter_messages('群名称',limit=10):

            time.sleep(2)
            print(message)

    except Exception as e:
        print(e)
    finally:

        client.disconnect()






if __name__ == '__main__':
    for userkey, userdatavlue in testinfo.items():
        getrun(userdatavlue)


