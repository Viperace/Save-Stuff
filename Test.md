先登入系統
Login to system first

您必须先登入系统才可以使用此功能 登陆
To use this feature, please login to system first |	Login

计


算购买ADS的数量
Calculate ADS amount to buy

充值后请先检查您的钱包是否有付款记录,如果存在,请等待确认
After topup, please check your wallet to confirm the payment record. If the record exists, please wait for further confirmation


兑换记录
Record of previous exchanges

请在 19:31 时间内完成支付
Please complete the transaction by 19:31

支付后先到到充值历史按"刷新"查看
After payment, please goto Topup History and tab "Refresh" to view your record

复制BTC地址
Copy BTC address

手动查询
Manual enquiry


0次确认代表BTC已经正常发送,小于0.01BTC兑换1次确认到帐,
0.1BT以内兑换需要3次确认到帐,
其他大额兑换必须6次或以上确认才可以到帐,
每次确认时间大约10分钟,具体速度会根据您钱包的矿工费用而定
0 confirmation means BTC has been sent.
Transaction under 0.01 BTC requires 1 confirmation.
Transaction under 0.1 BTC requires 3 confirmations.
Other larger transaction requires at least 6 confirmations.
Every confirmation requires around 10 minutes, actual speed will depend on your wallet settings and mining fees

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


