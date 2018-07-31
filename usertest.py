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
def useraddcoin(renshu):
    Extend_userdata=Extend_user.objects.all()[:renshu]
    for indd in Extend_userdata:
        print indd.username
        if random.randint(0, 6)>3:
            betquota=random.randint(100, 3000)
            if indd.xcoin>=betquota:
                Extend_useredit=Extend_user.objects.get(username=indd.username)
                Extend_useredit.xcoin=int(indd.xcoin)-int(betquota)
                Extend_useredit.save()
            bettingup.objects.get_or_create(
                userid=indd.ext_user_id,
                telid=indd.telid,
                betquota=betquota,
            )
            print 'up'
        else:
            betquota=random.randint(100, 3000)
            if indd.xcoin>=betquota:
                Extend_useredit=Extend_user.objects.get(username=indd.username)
                Extend_useredit.xcoin=int(indd.xcoin)-int(betquota)
                Extend_useredit.save()
            bettingdwon.objects.get_or_create(
                userid=indd.ext_user_id,
                telid=indd.telid,
                betquota=betquota,
            )
            print 'down'


# 删除所有用户
def deluser():
    Extend_user.objects.all().delete()
    User.objects.all().delete()
    bettingup.objects.all().delete()
    bettingdwon.objects.all().delete()


if __name__ == '__main__':
    ##创建100个用户每个人10000xcoin
    ##------------------------------------
    # for indd in xrange(0,10):
    #     cuser()
    #     print "userok"
    ##------------------------------------
    ##模拟下注
    useraddcoin(10)
    ##------------------------------------
    ## 清空用户
    # deluser()