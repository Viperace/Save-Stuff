
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


}


