#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import gevent

import os
import random
import sys
import platform

import time
import redis
import pandas as pd
import numpy
import pytz, datetime


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
    #os.chdir(r'J:\2017work\django\2018work\telegrambot\btc')
    sys.path.append(r'D:\Telegram Projects\TestModels 2\btc')
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

def createname():
    # 以openid方式创建用户
    # 因为只有openid没用户名所以随机生成用户名
    numnunber = random.randint(999, 900000000)
    try:
        User.objects.get(username=numnunber)
        createname()
    except:
        return numnunber


# 创建用户
def cuser():
    try:
        password = random.randint(10000, 99999)
        name = createname()
        creatuser = User.objects.create_user(username=name, password=str(password))
        Extend_user.objects.get_or_create(ext_user_id=creatuser.id,
                                          username=str(name),
                                          pawword=password,
                                          telid=str(name) + '_aa',
                                          openid=str(name) + '_aa',
                                          xcoin=100000,
                                          btcaddress=str(name) + '_no',
                                          giveusermoney=300,
                                          notice='大家好',
                                          isreferee=False,
                                          userisrun=False, )
    except:
        User.objects.filter(id=creatuser.id).delete()
        print "Fail to create"


# 模拟用户下注
def simulate_random_user_bet_OLD(renshu):
    Extend_userdata = Extend_user.objects.all()[:renshu]

    total_up_bet = 0
    total_down_bet = 0
    for indd in Extend_userdata:
        roll = random.randint(0, 100)
        betquota = random.randint(100, 3000)
        if roll > 51:
            if indd.xcoin >= betquota:
                Extend_useredit = Extend_user.objects.get(username=indd.username)
                Extend_useredit.xcoin = int(indd.xcoin) - int(betquota)
                Extend_useredit.save()
                bettingup.objects.get_or_create(
                    userid=indd.ext_user_id,
                    telid=indd.telid,
                    betquota=betquota,
                )
                total_up_bet += betquota

                print indd.username + ' bet up ' + str(betquota)
            else:
                print indd.username + ' not enough to bet '
        elif roll < 49:
            if indd.xcoin >= betquota:
                Extend_useredit = Extend_user.objects.get(username=indd.username)
                Extend_useredit.xcoin = int(indd.xcoin) - int(betquota)
                Extend_useredit.save()
                bettingdwon.objects.get_or_create(
                    userid=indd.ext_user_id,
                    telid=indd.telid,
                    betquota=betquota,
                )
                total_down_bet += betquota

                print indd.username + ' bet down ' + str(betquota)
            else:
                print indd.username + ' not enough to bet '
        else:
            print indd.username + ' no bet.'

    # Output
    output = [total_up_bet + total_down_bet, total_up_bet, total_down_bet]

    return output


def tally_total_xcoin(renshu):
    """Function to tally all coins in the game economy"""
    Extend_userdata = Extend_user.objects.all()[:renshu]

    total_coin = 0
    individual_coin_vec = []
    for indd in Extend_userdata:
        total_coin += indd.xcoin
        individual_coin_vec.append(indd.xcoin)

    return [total_coin, individual_coin_vec]


# This is a bot, that keep asking for gevent
# Once allow redist.get('allow_betting') = true, it will simulate place bet
"""Define a set of bettors, register their attribute
    - xcoin
    - Betting Range [low, high]
    - Bet Time Range [0, 30]  
Method required:
    - Listener
    - Bet placer
    - Tally
    - GetReportForUser(x)
"""


# VECTORIZE Version
def simulate_random_user_bet(renshu, exclude_list=[]):
    """ renshu, number of simulated bettors
        exclude_list, list of telid to be excluded
     """
    # Pre-Generate random bet size and direction first
    print "Simulating bets"
    bet_sizes = []
    bet_directions = []
    total_up_bet = 0  # Record purpose
    total_down_bet = 0
    for i in range(1, renshu + 1):
        # Gen size (conditional on have bet)
        betquota = random.randint(100, 3000)

        # Gen direction
        roll = random.randint(0, 100)
        if roll > 51:
            bet_directions += ["up"]
            total_up_bet += betquota
        elif roll < 48:
            bet_directions += ["down"]
            total_down_bet += betquota
        else:
            bet_directions += ["0"]
            betquota = 0

        bet_sizes += [betquota]

    # SET SPECIAL USER RULE
    # TODO: do at parameter
    robot_ind = 17
    bet_sizes[robot_ind] = 100
    bet_directions[robot_ind] = "both_side"
    robot17 = Extend_user.objects.get(pk=robot_ind+1)
    robot17.xcoin -= 100
    robot17.save()

    # Update user balance, to take away their xcoin as bet
    print "Minus user pocket"
    for i in range(1, renshu + 1):
        # Check if user has balance available for bet
        #user = Extend_user.objects.get(pk=i)
        user = Extend_user.objects.all()[i]
        if user.telid not in exclude_list:
            new_xcoin = int(user.xcoin) - int(bet_sizes[i - 1])
            print i
            # Save new balance if enough. Remove bet from vector if not enough
            if new_xcoin >= 0:
                Extend_user.objects.filter(pk=i).update(xcoin=new_xcoin)
            else:
                bet_sizes[i-1] = 0
                bet_directions[i-1] = "0"

    # Create bet down user list, following the generated sizes
    print "Write ticket to user"
    down_list = []
    up_list = []
    for i in range(1, renshu + 1):
        #indd = Extend_user.objects.get(pk=i)
        indd = Extend_user.objects.all()[i]

        if indd.telid not in exclude_list:
            if bet_directions[i-1] == "up":
                up_list.append(bettingup(
                    userid=indd.ext_user_id,
                    telid=indd.telid,
                    betquota=bet_sizes[i - 1]))
            elif bet_directions[i-1] == "down":
                down_list.append(bettingdwon(
                    userid=indd.ext_user_id,
                    telid=indd.telid,
                    betquota=bet_sizes[i - 1]))
            elif bet_directions[i-1] == "both_side":
                up_list.append(bettingup(
                    userid=indd.ext_user_id,
                    telid=indd.telid,
                    betquota=bet_sizes[i - 1]))
                down_list.append(bettingdwon(
                    userid=indd.ext_user_id,
                    telid=indd.telid,
                    betquota=bet_sizes[i - 1]))

    print "Bulk Update"
    # Bulk Update
    bettingup.objects.bulk_create(up_list)
    bettingdwon.objects.bulk_create(down_list)

    print "Done..."

    # Output
    output = [total_up_bet + total_down_bet, bet_sizes, bet_directions]

    return output


# Function to write and append to existing file
def appendDFToCSV_void(df, csvFilePath, sep=","):
    import os
    if not os.path.isfile(csvFilePath):
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep)
    elif len(df.columns) != len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns):
        raise Exception("Columns do not match!! Dataframe has " + str(len(df.columns)) + " columns. CSV file has " + str(len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns)) + " columns.")
    elif not (df.columns == pd.read_csv(csvFilePath, nrows=1, sep=sep).columns).all():
        raise Exception("Columns and column order of dataframe and csv file do not match!!")
    else:
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep, header=False)


def Run_Simulation(TOTAL_ROUND, NUM_USER, EXC_LIST = []):
    # Set testing parameter
    # Create a big ass (TOTAL_ROUND * Nuser matrix) * N_field matrix
    # Field has 1) bet size , 2) direction, 3) gain size

    # Initialize Recorder
    total_coin_vec = []  # Total coin in the system
    bet_amount_vec = []
    round_vec = []
    wealth_matrix = []  # Matrix that record all TxN, T round and N user
    bet_dirs_matrix = []
    bet_sizes_matrix = []

    # Start the testing loop
    has_bet_this_round = False
    round_index = 0
    while round_index < TOTAL_ROUND:
        # If betting allowed and user has not yet bet, then allow betting
        allow_betting = str(redisdb.get('gameBet')) == "yes"
        if not has_bet_this_round and allow_betting:
            round_index += 1
            has_bet_this_round = True
            print 'Round: ' + str(round_index)

            # Tally total coin
            totCoin, individual_coin = tally_total_xcoin(NUM_USER)

            # Simulate bet
            total, bet_sizes, bet_dirs = simulate_random_user_bet(NUM_USER, EXC_LIST)

            # Save files
            bet_amount_vec += [total]
            round_vec += [round_index]
            total_coin_vec += [totCoin]

            try:
                output_df = pd.DataFrame({'Round': [round_index], 'total_coin': [totCoin], 'bet amount': [total]})
                appendDFToCSV_void(output_df, file_name)
                wealth_matrix.append(individual_coin)
                bet_dirs_matrix.append(bet_dirs)
                bet_sizes_matrix.append(bet_sizes)

                #TODO: This rewrite entire matrix, not ideal. Should make append
                temp1 = numpy.asarray(wealth_matrix)
                numpy.savetxt("wealth_matrix.csv", temp1, delimiter=",")

                temp2 = numpy.asarray(bet_dirs_matrix)
                numpy.savetxt("Betdir_matrix.csv", temp2, delimiter=",", fmt="%s")

                temp3 = numpy.asarray(bet_sizes_matrix)
                numpy.savetxt("Betsize_matrix.csv", temp3, delimiter=",")
            except:
                print "Can't save. Please check"

        # If at Game_End stage, we may reset user place bet status
        at_gamesEnd = str(redisdb.get('gamesEnd')) == "end"
        if has_bet_this_round and at_gamesEnd:
            has_bet_this_round = False


    # Print
    # output_df.to_csv(file_name, sep=',')
    print "FINISH SIMULATION..."


def check_index():
    file_name = 'Index_log.csv'
    df = pd.DataFrame({'Time': [0], 'Final': [0], 'Fixed': [0]})
    appendDFToCSV_void(df, file_name)

    while True:
        print "Record time..."
        time.sleep(20)
        time_stamp = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
        netnumber_data = netnumber.objects.get(id=1)
        fixed = netnumber_data.fixednumber
        final = netnumber_data.finalnumber
        df = pd.DataFrame({'Time': [time_stamp], 'Final': [final], 'Fixed': [fixed]})
        appendDFToCSV_void(df, file_name)


# 删除所有用户
def deluser():
    Extend_user.objects.all().delete()
    User.objects.all().delete()
    bettingup.objects.all().delete()
    bettingdwon.objects.all().delete()


# Spawn separate thread to check index
gevent.spawn(check_index)


if __name__ == '__main__':
    ##创建100个用户每个人10000xcoin
    ##------------------------------------
    #for indd in xrange(0, 100):
    #    cuser()
    #    print "userok"
    ##------------------------------------

    ##模拟下注
    # Init recorder
    file_name = 'Bet_Log.csv'
    output_df = pd.DataFrame({'Round': [0], 'total_coin': [0], 'bet amount': [0]})
    appendDFToCSV_void(output_df, file_name)

    # Define list
    exc_list = ['574561150',    # VH Telid
                '605090514',    # YCQ Telid
                '537063173'     # VH3 Telid
                ]
    Run_Simulation(TOTAL_ROUND=1000, NUM_USER=20, EXC_LIST=exc_list)

    ##------------------------------------
    ## 清空用户
    # deluser()
