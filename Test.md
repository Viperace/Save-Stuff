usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys
import platform
import urllib

from netunit import myGet


reload(sys)
sys.setdefaultencoding('utf-8')
# django------------------------------------------------------------>
def isLinuxSystem():
    return 'Linux' in platform.system()


# 启动内存数据库
from myredis import redisfu, domain, serverpath, both5domain,mypc,channel,groupname, valuetoxcoin, xcointobtc,zhname,CustomScale, \
    websocketioippro

redisdb = redisfu()


# 通讯密钥
WEB_KEY = 'dfvSDF!KK080MJSDC'

if isLinuxSystem():
    # sys.path.append(r'/var/www/html/btc')
    # os.chdir(r'/var/www/html/btc')
    sys.path.append(serverpath)
    os.chdir(serverpath)
else:
    sys.path.append(mypc)
    os.chdir(mypc)

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, run_async
from telegram import ReplyKeyboardMarkup

import telegram

# bug探测
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#错误输出
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


#start启动的屏幕键盘
# 通用的下键盘
def downkeydate(bot, update):
    reply_keyboard = [['进入ADSCoin'], ['认 购','采 矿'], ['中文汉化', '翻 墙'],['邀请朋友','English/中文']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    #键盘按键
    update.message.reply_text('%s'%(zhname), reply_markup=markup, )



#和机器人对话
@run_async
def echo(bot, update):
    """Echo the user message."""

    print update.message.text
    # 当不是组聊天的时候
    if update.message.chat.type != 'supergroup':

        if update.message.text == '认 购':
            keyboard = [[InlineKeyboardButton("进入ADSCoin认购", url='http://www.adscoin.shop/wallet/buysell/')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('ADSCoin官方站点!', reply_markup=reply_markup, )

        if update.message.text == '进入ADSCoin':
            bothtml(bot, update)
            #更新头像
            botusermesgrun(bot,update)

        if update.message.text == '采 矿':
            keyboard = [[InlineKeyboardButton("进入采矿任务", url='http://www.adscoin.shop/mining.html')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('ADSCoin采矿', reply_markup=reply_markup, )

        if update.message.text == 'English/中文':
            pass

        if update.message.text == '中文汉化':
            # update.message.reply_text('https://t.me/zh_CN/465')
            bot.send_document(chat_id=update.message.chat_id,
                              caption='Android(安卓手机)\n使用方法: 点击上方蓝色的“↓”按钮下载，完成之后点击消息上的三个小灰点，选择 Apply localization file (使用本地化文件)',
                              document=open('btchtm/static/zh/Android.xml', 'rb'))
            bot.send_document(chat_id=update.message.chat_id,
                              caption='Windows,Linux,macOS\n使用方法:进入Settings(设置)，键盘上按住Alt+Shift，然后点击"Change Language（更改语言）"\n\n在macOS环境下安装翻译时，请确保语言文件存放在Download文件夹。',
                              document=open('btchtm/static/zh/TDesktop.strings', 'rb'))
            bot.send_document(chat_id=update.message.chat_id,
                              caption='苹果手机(IOS)\n使用方法: 点击上方蓝色的“↓”按钮下载，下载之后点击文件，选择 Apply localization (使用本地化)\n应用后有“可能会出现错误提示”，请点击 OK 忽略',
                              document=open('btchtm/static/zh/AppleiOS.strings', 'rb'))

        if update.message.text == '翻 墙':
            bot.send_message(chat_id=update.message.chat_id,
                             text='<a href="https://t.me/proxy?server=jp.3412.ml&port=9981&secret=030c0046b23166a31321f563e9883b81">1号服务器\n点这里自动配置到您的Telegram</a>\n\n<a href="https://t.me/proxy?server=jp.telepro.cf&port=9981&secret=c70ecdabfb228573d81de2dbf53ac0e3">2号服务器\n点这里自动配置到您的Telegram</a>\n\n<b>Telegram专用翻墙工具,永久高速免费,上Telegram专用</b>',
                             parse_mode=telegram.ParseMode.HTML)



        if update.message.text == '邀请朋友':
            share(bot, update)

#机器人个人信息获取
def botusermesg(bot,update):
    if update.message.from_user.username:
        telusername=update.message.from_user.username
    else:
        telusername=''

    if update.message.from_user.first_name:
        first_name=update.message.from_user.first_name
    else:
        first_name=''

    if update.message.from_user.last_name:
        last_name=update.message.from_user.last_name
    else:
        last_name=''
    if last_name:
        nickname = first_name+' '+last_name
    else:
        nickname=first_name
    if update.message.from_user.language_code:
        language = update.message.from_user.language_code
    else:
        language='None'

    try:
        # 有头像
        headimagefile_id = (update.message.from_user.get_profile_photos())['photos'][0][0]['file_id']
        # print headimagefile_id
        # print bot.get_user_profile_photos(update.message.chat_id)
        photo_file = bot.get_file(headimagefile_id)
        headimage = str(update.message.chat_id) + '_head.jpg'
        photo_file.download('./media/' + headimage)
    except:
        # 无头像
        headimage = 'nohead.jpg'
    return nickname,language,headimage,telusername

def botusermesgrun(bot,update):
     #每24小时更新一次头像和昵称
        if not redisdb.get('botusermesgtime'):
            #更新头像
            botusermesgdata=botusermesg(bot,update)
            nickname=botusermesgdata[0]
            language=botusermesgdata[1]
            headimage=botusermesgdata[2]
            telusername=botusermesgdata[3]
            nickname=urllib.quote(nickname.encode('utf-8'))
            myGet(domain + '/btchtm/updateTeleusermore/?telid=%s&nickname=%s&language=%s&headimage=%s&telusername=%s&key=%s' % (
            update.message.chat_id,nickname, language, headimage,telusername, WEB_KEY))
            redisdb.set('botusermesgtime', 'botusermesgtime', ex=60*60*24)

# 机器人开始
# https://telegram.me/vpnfreebot?start=abcde
@run_async
def start(bot, update, args):
    if update.message.chat.type != 'supergroup':
        telid = update.message.chat_id
        # print telid
        botusermesgdata=botusermesg(bot,update)
        nickname=botusermesgdata[0]
        language=botusermesgdata[1]
        headimage=botusermesgdata[2]
        telusername=botusermesgdata[3]
        try:
            # 获取推荐者id
            # print args[0]
            upid = str(args[0])
            # print upid
        except Exception,e:
            print e
            upid = 'None'
        try:
            nickname=urllib.quote(nickname.encode('utf-8'))
            myGetdata = myGet(domain + '/botsign/?telid=%s&upid=%s&nickname=%s&language=%s&headimage=%s&telusername=%s&key=%s' % (
            telid, upid, nickname, language, headimage,telusername, WEB_KEY))
            Getdata = json.loads(myGetdata)
            if (Getdata['data'] == 'userok'):
                # 启动菜单
                downkeydate(telid, update)
                # screendata(telid, update)
            else:
                # print 'a'
                update.message.reply_text('ADSCoin登入失败点这里再试一次 /start')
        except Exception,e:
            print e
            # print 'b'
            update.message.reply_text('ADSCoin登入失败点这里再试一次 /start')


#分享赚钱
def share(bot, update):
    telid = update.message.chat_id
    myGetdata = myGet(domain + '/botshare/?telid=%s&key=%s&language=%s' % (telid, WEB_KEY,'zh'))
    Getdata = json.loads(myGetdata)
    update.message.reply_text('您可以把以下贴子分享给您的朋友,一起加入ASDCoin 成功邀请赠送ADS ↴')
    bot.send_photo(chat_id=update.message.chat_id, photo='http://www.adscoin.shop/static/ad/adsad_1.jpg',caption=Getdata['data'],parse_mode=telegram.ParseMode.HTML)



#进入adsh5
def bothtml(bot, update):
    telid = update.message.chat_id
    myGetdata = myGet(domain + '/bothtml/?telid=%s&key=%s' % (telid, WEB_KEY))
    Getdata = json.loads(myGetdata)
    # print Getdata
    keyboard = [[InlineKeyboardButton("10秒内点击进入ADSCoin", url=websocketioippro + '/sign/%s/%s/' % (
    Getdata['data']['username'], Getdata['data']['password'])), ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('登陆钱包,都由此进入!', reply_markup=reply_markup, )

# 机器人启动入口
def main():
    # proxy = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:1080')
    # bot = telegram.Bot(token=TOKEN, request=proxy);
    # 用token登陆telegram
    # updater = Updater("479394151:AAFTsRMs12l9-tLXIc_aQ6PTHLrKG5_nw4Y",request_kwargs={'proxy_url': 'http://127.0.0.1:1088/'})#@sumisorabot

    # @ads_coinbot
    # zaijidi
    if isLinuxSystem():
        updater = Updater(token="764371140:AAH7kHMOWY7zLRrXQN39_1uc_Ou1UduP4kk")
    else:
        updater = Updater(token="764371140:AAH7kHMOWY7zLRrXQN39_1uc_Ou1UduP4kk",
                          request_kwargs={'proxy_url': 'http://127.0.0.1:1080/'})
    #处理start
    updater.dispatcher.add_handler(CommandHandler('start', start, pass_args=True, ))
    #处理start 的button回调
    # updater.dispatcher.add_handler(CallbackQueryHandler(button))
    #处理用户打字回应
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.dispatcher.add_error_handler(error)

    #定时队列
    # updater.job_queue.run_repeating(publicuserloop, interval=3, )

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
    # gevent.spawn(gametime, 5)




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


