
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

# *********************************************
import asyncio
import telethon.sync

loop = asyncio.get_event_loop()

# *********************************************
# VH: Aysnc method to loop message
async def myjob(client):
  async for message in client.iter_messages('gamesoftboy',limit=10):
    await asyncio.sleep(1)
    print(message)


testinfo = {
# 申请api接口
# https://my.telegram.org/apps
#电话号码,电话号码,api ,key
    '91094016': ('91094016', 12345, 'd73xd14f8a78xcfr5692ec93f19'),
}


def getrun(value):
    # +86这里我是填中国你可以填新加坡的
    print('+65' + str(value[0]))
    print('>>>>loading...')
    try:
        #client = TelegramClient(*value)
        api_id = 12345
        api_hash = 'd73xd14f8a78xcfr5692ec93f19'
        client = TelegramClient('TestSession', api_id, api_hash).start()

        print('>>>>ok...')
        if not client.is_user_authorized():
            print('>>>> client  not !')
            raise

        # *********************************************
        print('retreiving async...')        
        loop.run_until_complete(myjob(client))
        

    except Exception as e:
        print(e)
    finally:
        print(client)
        #client.disconnect()



if __name__ == '__main__':
    for userkey, userdatavlue in testinfo.items():
        a = userkey
        b = userdatavlue
        getrun(userdatavlue)

