#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import sys
import platform


reload(sys)
sys.setdefaultencoding('utf-8')
# django------------------------------------------------------------>
def isLinuxSystem():
    return 'Linux' in platform.system()


if isLinuxSystem():
    sys.path.append(r'/var/www/html/btc')
    os.chdir(r'/var/www/html/btc')
else:
    sys.path.append(r'J:\2017work\django\2018work\telegrambot\btc')
    os.chdir(r'J:\2017work\django\2018work\telegrambot\btc')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btc.settings')
import django
# 当前时间时区
from django.utils import timezone
# 这里显示不正常也没关系其实他已经在操作django模型只是没目录看起来会报错.但是目录已经通过上面的配置引入
from btchtm.models import Extend_user, bettingup, bettingdwon
from django.contrib.auth.models import User
def createname():
    # 以openid方式创建用户
    #因为只有openid没用户名所以随机生成用户名
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
                                          telid=str(name)+'_aa',
                                          openid=str(name)+'_aa',
                                          xcoin=100000,
                                          btcaddress=str(name) + '_no',
                                          giveusermoney=300,
                                          notice='大家好',
                                          isreferee=False,
                                          userisrun=False, )
    except:
        User.objects.filter(id=creatuser.id).delete()


# 模拟用户下注
def simulate_random_user_bet(renshu):
    Extend_userdata=Extend_user.objects.all()[:renshu]
	
	total_up_bet = 0
	total_down_bet = 0
    for indd in Extend_userdata:	
		roll = random.randint(0, 100)
		betquota=random.randint(100, 3000)
        if roll > 51:            
            if indd.xcoin>=betquota:
                Extend_useredit=Extend_user.objects.get(username=indd.username)
                Extend_useredit.xcoin=int(indd.xcoin)-int(betquota)
                Extend_useredit.save()
				bettingup.objects.get_or_create(
					userid=indd.ext_user_id,
					telid=indd.telid,
					betquota=betquota,
				)				
				total_up_bet += betquota
				
				print indd.username + ' bet up ' + str(betquota )
			else:
				print indd.username + ' not enough to bet '
        elif roll < 49:
            if indd.xcoin>=betquota:
                Extend_useredit=Extend_user.objects.get(username=indd.username)
                Extend_useredit.xcoin=int(indd.xcoin)-int(betquota)
                Extend_useredit.save()
				bettingdwon.objects.get_or_create(
					userid=indd.ext_user_id,
					telid=indd.telid,
					betquota=betquota,
				)
				total_down_bet += betquota
				
				print indd.username + ' bet down ' + str(betquota )
			else:
				print indd.username + ' not enough to bet '
		else:
			print indd.username + ' no bet.'
			
	# Output
	output = [total_up_bet + total_down_bet, total_up_bet, total_down_bet]
	
	return output
			
# Function to check all coins lost
def tally_total_xcoin():
	Extend_userdata=Extend_user.objects.all()
	total_coin = 0
    for indd in Extend_userdata:
        total_coin += indd.xcoin
		
	return total_coin

	
# Function to check all coins lost
class BetSimulationTester:
	bettors = []
	
	__init__(self):
		return self
		
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
	
	def Simulate_Bet_Placing():
		return
	
	


# 删除所有用户
def deluser():
    Extend_user.objects.all().delete()
    User.objects.all().delete()
    bettingup.objects.all().delete()
    bettingdwon.objects.all().delete()

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
redisdb = redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    ##创建100个用户每个人10000xcoin
    ##------------------------------------
    # for indd in xrange(0,10):
    #     cuser()
    #     print "userok"
    ##------------------------------------
    ##模拟下注
	# Set testing parameter
	TOTAL_ROUND = 200
	
	# Initialize Recorder
	total_coin_vec = []		# Total coin in the system
	bet_amount_vec = []
	round_vec = []
	
	# Create a big ass (TOTAL_ROUND * Nuser matrix) * N_field matrix
	# Field has 1) bet size , 2) direction, 3) gain size 
	
	# Start the testing loop
	has_bet_this_round = False
	round_index = 0
	while round_index < TOTAL_ROUND:	
		# If betting allowed and user has not yet bet, then allow betting
		allow_betting = str(redisdb.get('gameBet')) == "Yes"
		if not has_bet_this_round and allow_betting:	
			round_index++
			has_bet_this_round = True
			
			# Simulate bet
			total, total_up, total_down = simulate_random_user_bet(10)
			
			# Tally & Save						
			bet_amount_vec += total
			round_vec += round_index
			total_coin_vec += tally_total_xcoin()
		
		# If at Game_End stage, we may reset user place bet status
		at_gamesEnd = str(redisdb.get('gamesEnd')) == "end"
		if has_bet_this_round and at_gamesEnd:
			has_bet_this_round = False
			
		time.sleep(1) 
		

    ##------------------------------------
    ## 清空用户
    # deluser()
