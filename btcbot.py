#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import sys
import platform
from urllib import unquote
import datetime, time
import redis
import telegram

reload(sys)
sys.setdefaultencoding('utf-8')
# django------------------------------------------------------------>
def isLinuxSystem():
    return 'Linux' in platform.system()


if isLinuxSystem():
    sys.path.append(r'/var/www/html/btc')
    os.chdir(r'/var/www/html/btc')
else:
    #sys.path.append(r'J:\2017work\django\2018work\telegrambot\btc')
    sys.path.append(r'D:\Telegram Projects\TestModels 2\btc')
    #os.chdir(r'J:\2017work\django\2018work\telegrambot\btc')
    os.chdir(r'D:\Telegram Projects\TestModels 2\btc')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btc.settings')
import django

django.setup()
# 当前时间时区
from django.utils import timezone
# 这里显示不正常也没关系其实他已经在操作django模型只是没目录看起来会报错.但是目录已经通过上面的配置引入
from btchtm.models import Extend_user, bettingup, bettingdwon, winning, netnumber
from django.contrib.auth.models import User
#django------------------------------------------------------------>

#启动内存数据库
#pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
pool = redis.ConnectionPool(host='155.254.49.141',password='#$dsd!4ds', port=6379, decode_responses=True)
redisdb = redis.Redis(connection_pool=pool)

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, \
    RegexHandler
from telegram import ReplyKeyboardMarkup

import telegram
import pytz

#bug探测
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义全局变量
myglobal = ''



#游戏时间
def gamesStartTime():
    seconds = redisdb.ttl('gamesStart')
    if seconds:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return str(("%02d:%02d" % (m, s)))
    else:
        return '00:00'

#等待开奖时间
def gamesYeidTime():
    seconds = redisdb.ttl('gamesYeid')
    if seconds:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return str(("%02d:%02d" % (m, s)))
    else:
        return '00:00'

#聊天时间
def gamesEndTime():
    seconds = redisdb.ttl('gamesEnd')
    if seconds:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return str(("%02d:%02d" % (m, s)))
    else:
        return '00:00'


# 是否可以投注的装饰器
def isbet(inputfuc):
    def fuc(bot,update):
        gamesYeid = str(redisdb.ttl('gamesYeid'))
        gamesEnd = str(redisdb.ttl('gamesEnd'))
        gameBet = str(redisdb.get('gameBet'))

        if str(gameBet) == 'yes':
            starttime = gamesStartTime()
            update.message.reply_text('现在是投注时间请您随意投注祝您好运.\n距离停止投注剩余 : ' + starttime+' 秒')
            inputfuc(bot,update)
            # return True
        else:
            if gamesYeid != 'None':
                yeidtime = gamesYeidTime()
                update.message.reply_text('投注已停止,下注已无法,请等待开奖.\n开奖时间还剩余 : ' + yeidtime+' 秒')
            elif gamesEnd != 'None':
                endtime = gamesEndTime()
                update.message.reply_text('本期投注已开奖请查看开奖记录\n距离下次投注时间 : ' + endtime+' 秒')
            # return False
    return fuc


#start启动的屏幕键盘
# 通用的下键盘
def downkeydate(bot, update):
    reply_keyboard = [['开始下注', '开 奖', '充 值', '收 款'], ['中 文', '翻 墙'], ['游戏规则'], ['邀请朋友一起玩']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    # print markup
    #键盘按键
    update.message.reply_text('欢迎光临比特娱乐:', reply_markup=markup, )


def screendata(chat_id, update):
    # 屏幕按键
    keyboard = [[InlineKeyboardButton(unquote("游戏玩法"), callback_data='menuhelp'), ],
                [InlineKeyboardButton("充值教学", callback_data='menuaddpoint')],
                [InlineKeyboardButton("开始下注", callback_data='gamestart')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('您好我是比特币投注机器人:', reply_markup=reply_markup, )


# 买涨

def touzhuup(bot, update):
    myglobal = 0
    reply_keyboard = [['↑+100', '↑+200', '↑+500', '↑+1K', '↑+3K'],['↑+全梭了','投注详情'], ['↑买涨', '↓买跌'], ['✖↑取消'], ['♜主页']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    try:
        Extend_userdata = Extend_user.objects.get(telid=update.message.chat_id)
        print Extend_userdata.xcoin
        update.message.reply_text('您的余额是 : %s X币\n选择您要下注的数额' % (str(Extend_userdata.xcoin)), reply_markup=markup)
    except:
        print "Error in Extend_user.objects.get(telid=update.message.chat_id)"


#买跌
def touzhudown(bot, update):
    myglobal = 1
    reply_keyboard = [['↓+100', '↓+200', '↓+500', '↓+1K', '↓+3K'],['↓+全梭了','投注详情'], ['↑买涨', '↓买跌'], ['✖↓取消'], ['♜主页']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    try:
        Extend_userdata = Extend_user.objects.get(telid=update.message.chat_id)
        print Extend_userdata.xcoin
        update.message.reply_text('您的余额是 : %s X币\n选择您要下注的数额' % (str(Extend_userdata.xcoin)), reply_markup=markup)
    except:
        print "Error in Extend_user.objects.get(telid=update.message.chat_id)"


#买涨
@isbet
def buyhandleup(bot,update):
    usermessage = update.message.text
    usermessage = str(usermessage).split('↑+')
    if usermessage[1] == '100':
        mesgbuy(update, 0, 100)
    elif usermessage[1] == '200':
        mesgbuy(update, 0, 200)
    elif usermessage[1] == '500':
        mesgbuy(update, 0, 500)
    elif usermessage[1] == '1K':
        mesgbuy(update, 0, 1000)
    elif usermessage[1] == '3K':
        mesgbuy(update, 0, 3000)
    elif usermessage[1] == '全梭了':
        try:
            Extend_userdata=Extend_user.objects.get(telid=update.message.chat_id)
            mesgbuy(update, 0, Extend_userdata.xcoin)
        except:
            print "Error in Extend_user.objects.get(telid=update.message.chat_id)"


#买跌
@isbet
def buyhandledown(bot,update):
    usermessage = update.message.text
    usermessage = str(usermessage).split('↓+')
    if usermessage[1] == '100':
        mesgbuy(update, 1, 100)
    elif usermessage[1] == '200':
        mesgbuy(update, 1, 200)
    elif usermessage[1] == '500':
        mesgbuy(update, 1, 500)
    elif usermessage[1] == '1K':
        mesgbuy(update, 1, 1000)
    elif usermessage[1] == '3K':
        mesgbuy(update, 1, 3000)
    elif usermessage[1] == '全梭了':
        try:
            Extend_userdata=Extend_user.objects.get(telid=update.message.chat_id)
            mesgbuy(update, 1, Extend_userdata.xcoin)
        except:
            print "Error in Extend_user.objects.get(telid=update.message.chat_id)"


def mesgbuy(update, isupdown, betquota):
    try:
        Extend_userdata = Extend_user.objects.get(telid=update.message.chat_id)
        if betquota>=100:
            if isupdown == 0:
                if Extend_userdata.xcoin - betquota >= 0:
                    # 买涨
                    try:
                        bettingup.objects.get(telid=update.message.chat_id)
                    except:
                        bettingup.objects.get_or_create(userid=Extend_userdata.ext_user_id,
                                                        telid=Extend_userdata.telid,
                                                        betquota=0, )
                    Extend_userdata.xcoin = Extend_userdata.xcoin - int(betquota)
                    Extend_userdata.save()
                    bettingupdata = bettingup.objects.get(telid=update.message.chat_id)
                    bettingupdata.betquota = bettingupdata.betquota + betquota
                    bettingupdata.save()
                    update.message.reply_text(
                        '您的余额是 : %s X币\n买涨↑总下注%s' % (str(Extend_userdata.xcoin), str(bettingupdata.betquota)))
                else:
                    update.message.reply_text('您的余额是 : %s X币\n余额不足无法下注' % (str(Extend_userdata.xcoin)))

            # 买跌
            if isupdown == 1:
                if Extend_userdata.xcoin - betquota >= 0:
                    try:
                        bettingdwon.objects.get(telid=update.message.chat_id)
                    except:
                        bettingdwon.objects.get_or_create(userid=Extend_userdata.ext_user_id,
                                                          telid=Extend_userdata.telid,
                                                          betquota=0, )
                    Extend_userdata.xcoin = Extend_userdata.xcoin - int(betquota)
                    Extend_userdata.save()
                    bettingdwondata = bettingdwon.objects.get(telid=update.message.chat_id)
                    bettingdwondata.betquota = bettingdwondata.betquota + betquota
                    bettingdwondata.save()
                    update.message.reply_text(
                        '您的余额是 : %s X币\n买跌↓总下注 %s X币' % (str(Extend_userdata.xcoin), str(bettingdwondata.betquota)))
                else:
                    update.message.reply_text('您的余额是 : %s X币\n余额不足无法下注' % (str(Extend_userdata.xcoin)))
        else:
            update.message.reply_text('您的余额是 : %s X币\n投注最少 100 X币起' % (str(Extend_userdata.xcoin)))
    except:
        print "Error in Extend_user.objects.get(telid=update.message.chat_id)"

# 取消买涨
@isbet
def cancelup(bot,update):
    try:
        bettingupdata = bettingup.objects.get(telid=update.message.chat_id)
    except Exception, e:
        print e
    try:
        Extend_userdata = Extend_user.objects.get(telid=update.message.chat_id)
        Extend_userdata.xcoin = Extend_userdata.xcoin + int(bettingupdata.betquota)
        Extend_userdata.save()
        bettingupdata.delete()
        update.message.reply_text('您以取消本次买涨的所有下注\n反还 %s X币' % (bettingupdata.betquota))
    except Exception, e:
        print e
        update.message.reply_text('您未下注无需取消')


# 取消买跌
@isbet
def canceldown(bot,update):
    try:
        bettingdwondata = bettingdwon.objects.get(telid=update.message.chat_id)
    except Exception, e:
        print e
    try:
        Extend_userdata = Extend_user.objects.get(telid=update.message.chat_id)
        Extend_userdata.xcoin = Extend_userdata.xcoin + int(bettingdwondata.betquota)
        Extend_userdata.save()
        bettingdwondata.delete()
        update.message.reply_text('您以取消本次买跌的所有下注\n反还 %s X币' % (bettingdwondata.betquota))
    except Exception, e:
        print e
        update.message.reply_text('您未下注无需取消')


#和机器人对话
def echo(bot, update):
    isbet(update)
    """Echo the user message."""
    print update.message.text
    print update.message.chat_id
    # bot.send_message(chat_id=update.message.chat_id,text='<b>这是一张黄图</b><a href="http://www.w3school.com.cn/i/eg_tulip.jpg">link</a>', parse_mode=telegram.ParseMode.HTML)
    # update.message.reply_text(update.message.text ,photo='http://www.w3school.com.cn/i/eg_tulip.jpg')
    # bot.send_photo(chat_id=update.message.chat_id, photo='https://farm2.staticflickr.com/1680/24816754162_cbcf0268d7_c.jpg')
    # 注册被开启
    # openid = update.message.chat_id
    # bot.send_photo(chat_id=update.message.chat_id, photo='https://telegram.org/img/t_logo.png')
    if update.message.text == '♜主页':
        downkeydate(bot, update)
        screendata(update.message.chat_id, update)
    if update.message.text == '开始下注':
        # keyboard = [[InlineKeyboardButton(unquote("客户端下注内容更精彩"), url='http://127.0.0.1:8000/sing/'),]]
        keyboard = [[InlineKeyboardButton(unquote("客户端下注内容更精彩"), url='http://192.168.1.104:8000'), ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('您好我是比特币投注机器人:', reply_markup=reply_markup, )
        touzhuup(bot, update)
    # 买涨入口
    if update.message.text == '↑买涨':
        touzhuup(bot, update)
    #买跌入口
    if update.message.text == '↓买跌':
        touzhudown(bot, update)

    # 买涨
    if str(update.message.text).split('+')[0] == '↑':
        buyhandleup(bot,update)
    # 买跌
    if str(update.message.text).split('+')[0] == '↓':
        buyhandledown(bot,update)

    if update.message.text == '投注详情':
        betdetailed(bot,update)

    if update.message.text == '✖↑取消':
        cancelup(bot,update)

    if update.message.text == '✖↓取消':
        canceldown(bot,update)

    if update.message.text == '开 奖':
        pass
    if update.message.text == '充 值':
        pass
    if update.message.text == '收 款':
        # bot.send_photo(chat_id=update.message.chat_id, photo=open('images/help/sstutio.jpg', 'rb'))
        pass
    if update.message.text == '中 文':
        update.message.reply_text('https://t.me/zh_CN/462')
    if update.message.text == '翻 墙':
        bot.send_message(chat_id=update.message.chat_id,
                         text='<a href="https://t.me/proxy?server=155.254.49.141&port=443&secret=a0cbcef5a486d9636472ac27f8e11a9d">点这里自动安装到您的手机</a>\n<b>Telegram专用翻墙工具,永久高速免费,三天会更新一次,请按时回来更新,请不要把代理工具随意分享,人多了您就慢了切记</b>',
                         parse_mode=telegram.ParseMode.HTML)
        pass
    if update.message.text == '游戏规则':
        pass


def explore_username(update):
    """Function to get the representative name of the user. Starting from
     username, firstname, last name till we got it"""
    nickname = update.message.from_user.username
    if nickname:
        return nickname

    nickname = update.message.from_user.first_name
    if nickname:
        return nickname

    nickname = update.message.from_user.last_name
    if nickname:
        return nickname


# 机器人开始
# https://telegram.me/vpnfreebot?start=abcde
def start(bot, update, args):
    telid = update.message.chat_id

    # -------------------------获取头像------------------------------->
    try:
        # 获取用户昵称
        nickname = explore_username(update)

        headimagefile_id=(update.message.from_user.get_profile_photos())['photos'][0][0]['file_id']
        print headimagefile_id
        # print bot.get_user_profile_photos(update.message.chat_id)
        photo_file = bot.get_file(headimagefile_id)
        headimage=str(telid)+'_head.jpg'
        photo_file.download('./media/'+headimage)
    except:
        print "无头像. No avatar"
        pass
    # -------------------------获取头像------------------------------->

    try:
        Extend_user.objects.get(telid=telid)
        # 启动菜单
        screendata(telid, update)
        downkeydate(telid, update)
    except:
        try:
            password = random.randint(10000, 99999)

            if not nickname:
                name = createname()
            else:
                name = nickname
            print "this user has nickname " + nickname

            creatuser = User.objects.create_user(username=name, password=str(password))
            Extend_user.objects.get_or_create(ext_user_id=creatuser.id,
                                              username=str(name),
                                              pawword=password,
                                              telid=str(telid),
                                              openid=str(name) + str(telid),
                                              xcoin=0,
                                              btcaddress=str(name) + '_no',
                                              giveusermoney=300,
                                              notice='大家好',
                                              isreferee=False,
                                              userisrun=False, )
        except:
            User.objects.filter(id=creatuser.id).delete()

        try:
            username = str(args[0])
            Extend_userdata = Extend_user.objects.get(username=username)

        except:
            pass


#屏幕上的start button回调
def button(bot, update):
    query = update.callback_query
    #游戏玩法
    if query.data == 'menuhelp':
        query.message.reply_text(unquote('这个比特币指数投注机器人三分钟开奖一次,他可以让您赢取很多比特币,只有买涨和买跌,只要您买中了就可以获得不同赔率的奖金,赶快参加投注赢去无限奖金'))

    if query.data == 'menuaddpoint':
        query.message.reply_text(unquote('这里是充值教学'))

    #pc如何使用教学
    if query.data == 'gamestart':
        query.message.reply_text(unquote('开始下注'))
        # bot.send_photo(chat_id=query.message.chat_id, photo=open('images/help/sstutio.jpg', 'rb'))


        # bot.edit_message_text(text="Selected option: {}".format(query.data),
        #                       chat_id=query.message.chat_id,
        #                       message_id=query.message.message_id)


#错误输出
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def betdetailed(bot,update):
    upbetquota=''
    downbetquota=''
    try:
        bettingupdata=bettingup.objects.get(telid=update.message.chat_id)
        upbetquota=str(bettingupdata.betquota)
    except:
        upbetquota='0'

    try:
        bettingdwondata=bettingdwon.objects.get(telid=update.message.chat_id)
        downbetquota=str(bettingdwondata.betquota)
    except:
        downbetquota='0'

    try:
        windata = winning.objects.all()[1]
        print windata.iloc[0]['userup']
        print windata.iloc[0]['userdown']
        print windata.iloc[0]['quota']
        print windata.iloc[0]['theodds']
    except:
        ""

    try:
        Extend_userdata = Extend_user.objects.get(telid=update.message.chat_id)
        update.message.reply_text('您的投注详情\n余额 : %s X币\n当前个人投注如下:\n↑买涨 %s X币\n↓买跌 %s X币 \n'%(str(Extend_userdata.xcoin),upbetquota,downbetquota))
        update.message.reply_text('下注时间: ' + gamesStartTime() + '   开奖时间：' + gamesYeidTime())
    except:
        print "Error in Extend_user.objects.get(telid=update.message.chat_id)"


# 工具类------------------------------------->


def createname():
    # 以openid方式创建用户
    #因为只有openid没用户名所以随机生成用户名
    numnunber = random.randint(999, 900000000)
    try:
        User.objects.get(username=numnunber)
        createname()
    except:
        return numnunber


def get_winners_list(query_objects):
    """Function to return list of winners username """

    usernames = []
    betsizes = []
    for winner_object in query_objects:
        username = Extend_user.objects.get(telid=winner_object.telid).username
        usernames.append(username)

        betsize = winner_object.betquota
        betsizes.append(betsize)

    return usernames, betsizes


def announce_result(bot, job):
    """Function to announce results to bettors"""
    print "Announcement start here- " + str(datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')))

    # Fetch result
    netnumberdata = netnumber.objects.get(id=1)
    start_index = netnumberdata.fixednumber
    end_index = netnumberdata.finalnumber

    # Print result
    winners = []
    winner_sizes = []
    if end_index > start_index:
        #arrow = "上 ▲"
        arrow = "\n       ▲" + \
                "\n      ':'" + \
                "\n    ':::::'" + \
                "\n  ':::::::::'" + \
                "\n':::::::::::::'" + \
                "\n:::::::::::::::"
        winners, winner_sizes = get_winners_list(bettingup.objects.all())
    elif end_index < start_index:
        #arrow = "下 ▼"
        arrow = "\n:::::::::::::::" + \
                "\n':::::::::::::'" + \
                "\n  ':::::::::'" + \
                "\n    ':::::'" + \
                "\n      ':'" + \
                "\n       '"
        winners, winner_sizes = get_winners_list(bettingdwon.objects.all())
    else:
        arrow = "平 ==============="

    winners_str = u"\n~~~~~~~~~~ 恭喜胜利者 ~~~~~~~~~~~"
    for i in range(0, len(winners)):
        winners_str += "\n" + str(winners[i]) + " , " + str(winner_sizes[i])
    winners_str += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    if len(winning.objects.all()) > 0:  # Print
        nuser_up = winning.objects.values_list('userup', flat=True)[0]
        nuser_down = winning.objects.values_list('userdown', flat=True)[0]
        total_bet = winning.objects.values_list('quota', flat=True)[0]
        odds = winning.objects.values_list('theodds', flat=True)[0]

        if odds != 0:
            total_up_bet = odds * total_bet / (1 + odds)
            total_down_bet = total_up_bet / odds
            inverse_odds = 1/odds
        else:
            if nuser_up > 0 and nuser_down > 0:
                total_up_bet = "-"
                total_down_bet = "-"

            # Total up/down bet, and 1/odds
            elif nuser_up > 0:
                total_up_bet = int(odds * float(total_bet) / (1 + odds))
                total_down_bet = total_bet - total_up_bet
            else:
                total_up_bet = 0
                total_down_bet = total_bet - total_up_bet

            inverse_odds = 0

        msg = '买涨人数：' + str(nuser_up) + '\n买跌人数：' + str(nuser_down) + \
              '\n总注码：' + str(total_bet) + \
              '\n买上注码：' + str(total_up_bet) + '       买下注码：' + str(total_down_bet) + \
              '\n涨/跌：' + str(round(odds, 5)) + '       跌/涨：' + str(round(inverse_odds, 5)) + \
              '\n开' + str(start_index) + ',  结' + str(end_index)
        msg2 = arrow + winners_str
    else:
        msg = '...'
        msg2 = '.'

    # Get all up/down bettors, and send them message
    all_telid = list(bettingup.objects.values_list('telid', flat=True))
    all_telid += list(bettingdwon.objects.values_list('telid', flat=True))
    for telid in set(all_telid):
        try:
            bot.send_message(chat_id=telid, text=msg)
            bot.send_message(chat_id=telid, text=msg2)
        except Exception, e:
            print "Cant send message to this telid " + telid


def announce_result_loop(bot, job):
    """Scheduler to print bet outcome result & Delete"""
    # Run this loop that check for changes of state to 'gamesEnd'
    refresh_interval = 1
    while True:
        first_check_game_not_ended = redisdb.ttl('gamesYeid') > 0
        time.sleep(refresh_interval)

        second_check_game_ended = str(redisdb.ttl('gamesYeid')) == "None"
        if second_check_game_ended and first_check_game_not_ended:   # This check for game state 'JUST' changed
            # DO ANNOUNCEMENT HERE
            # announce_result(bot, job) # Sometimes got problem?
            job.job_queue.run_once(announce_result, when=2)   # Delay 2 secs to give server time

            # Schedule next result-announcement loop
            print "Schedule next announcement loop"
            job.job_queue.run_once(announce_result_loop, when=25 + 10 - 7)

            # Schedule next STOP-announcement #TODO: Delete this. Can't seem to follow time correctly
            # job.job_queue.run_once(announce_stop, when=25 - 10 - 1)  # earlier one sec
            break


def announce_stop(bot, job):
    """Function to announce STOP betting"""
    announce_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))

    msg = "买定离手 " + str(announce_time)
    print 'announcing ' + msg + ' ' + str(announce_time)

    # Get all up/down bettors, and send them message
    all_telid = list(bettingup.objects.values_list('telid', flat=True))
    all_telid += list(bettingdwon.objects.values_list('telid', flat=True))
    for telid in set(all_telid):
        try:
            bot.send_message(chat_id=telid, text=msg)
        except Exception, e:
            print "Cant print 买定离手 to " + telid


# 机器人启动入口
def main():
    # This is YCQ
    #updater = Updater(token="695084531:AAFczz_cSkdzx7RefbIsI-iHAKAa38qLbUE")
    updater = Updater(token="556371653:AAGTJ7uILwzBaD7nbSnYjqzYqiexZN4ivdM") # LVH

    #处理start
    updater.dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
    #处理start 的button回调
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    #处理用户打字回应
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.dispatcher.add_error_handler(error)

    # Queue for announcement
    updater.job_queue.run_once(announce_result_loop, when=25 + 10 - 7)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()



if __name__ == '__main__':
    main()
    # gevent.spawn(gametime, 5)