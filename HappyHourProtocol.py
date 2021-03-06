# -*- coding: utf-8 -*-

import pandas as pd
import redis
import datetime
import random
import math
import time
import numpy as np

# ***** django requirement *******
import sys
import os
import platform
import django

def isLinuxSystem():
    return 'Linux' in platform.system()

if isLinuxSystem():
    sys.path.append(r'/var/www/html/btc')
    os.chdir(r'/var/www/html/btc')
else:
    sys.path.append(r'D:\Telegram Projects\Telebet Live\btc')
    os.chdir(r'D:\Telegram Projects\Telebet Live\btc')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btc.settings')

django.setup()

#django------------------------------------------------------------>
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
redisdb = redis.Redis(connection_pool=pool)

from btchtm.models import Extend_user, bettingup, bettingdwon, netnumber
from django.contrib.auth.models import User


# ***** My class *******

class HappyCheater:
    outcome = None
    win_bet = None
    lose_bet = None
    ghost_book = []
    min_betsize = 100.0  # Constant param

    def __init__(self):
        self.data = []

    def __init__(self, outcome, win_bet, lose_bet, ghost_book):
        self.outcome = outcome
        self.win_bet = win_bet
        self.lose_bet = lose_bet
        self.ghost_book = ghost_book

    def get_min_winlose_size(self):
        """Get the optimal win/lose bet according to Golden Ratio
        """
        if self.lose_bet > 0:
            adj_lose_bet = self.min_betsize
            adj_win_bet = math.ceil(adj_lose_bet * self.win_bet / self.lose_bet)
            return adj_win_bet, adj_lose_bet
        elif self.lose_bet > 0 and self.win_bet == 0:
            # Sure win case, anything ratio you want
            return self.min_betsize, self.min_betsize
        elif self.lose_bet == 0 and self.win_bet > 0:
            # Sure lose case, must not put any on lose side
            return self.min_betsize, 0
        else:
            return 0, 0

    def allocate_ghosts(self):
        """ Return ghosts that will put more money on the losing side.

        Return two dataframes, one for up-side ghost, one for down side
        Dataframe is in (userid, telid, bet_size).
        """

        # Decide total free lunch to give
        if self.win_bet > 0:
            win_odds = self.lose_bet / self.win_bet
        else:
            win_odds = 0

        if win_odds > 1:
            adj_win_odds = win_odds * random.randrange(130, 150) * 0.01
        elif win_odds > 0.5:
            adj_win_odds = win_odds + random.randrange(30, 60) * 0.01
        elif win_odds > 0:
            adj_win_odds = win_odds + random.randrange(40, 90) * 0.01
        else:
            adj_win_odds = random.randrange(50, 150) * 0.01
        free_lunch_to_give = (adj_win_odds - win_odds) * self.win_bet
        free_lunch_to_give = round(free_lunch_to_give * 0.01) * 100

        bet_lose = free_lunch_to_give
        bet_win = round(bet_lose * random.randrange(40, 90)*0.01)

        # Round to 100
        bet_lose = round(bet_lose*0.01) * 100
        bet_win = round(bet_win*0.01) * 100

        # Randomize number of ghosts
        num_lost_ghost = random.randint(5, 20)
        num_win_ghost = random.randint(5, 20)

        # Create ghost characteristic
        print "Bet_lose " + str(bet_lose) + "  Bet_win " + str(bet_win)
        print "num_lost_ghost " + str(num_lost_ghost) + "  num_win_ghost " + str(num_win_ghost)
        losers_df = self.split_bet_across(bet_amount=bet_lose, N=num_lost_ghost, exclude_telid=[])
        winners_df = self.split_bet_across(bet_amount=bet_win, N=num_win_ghost, exclude_telid=[])

        print "Actual lost ghost: " + str(len(losers_df)) + "  Actual win ghost: " + str(len(winners_df))

        # Convert to up/down
        if self.outcome == "UP":
            ghost_up_df = winners_df
            ghost_down_df = losers_df
        elif self.outcome == "DOWN":
            ghost_up_df = losers_df
            ghost_down_df = winners_df
        else:
            print "Outcome is DRAW"
            ghost_up_df = losers_df
            ghost_down_df = winners_df

        return ghost_up_df, ghost_down_df

    def split_bet_across(self, bet_amount, N, exclude_telid=[]):
        """Split bet_amount across N different ghosts. 'exclude_telid' are ghost to be excluded
        Ensure each bet follow multiple of min_betsize

        return DataFrame
        """
        # Sanity check
        if bet_amount == 0:
            print "bet amt = 0. Nothing to split"
            return []
        elif N == 0:
            print "N = 0. Nothing to split"
            return []
        elif round(bet_amount / self.min_betsize) - (bet_amount / self.min_betsize) > 0.00001:
            print "bet_amount not multiple of bet_amount"
            return []
        else:
            npiece = int(bet_amount / self.min_betsize)

        # N cannot be larger than npiece
        if N > npiece:
            N = npiece

        print 'split: ' + str(npiece) + '  Npop:' + str(N)

        # Split the piece
        x = range(0, npiece)
        index = random.sample(x, N - 1)
        index = sorted(index)
        index.append(npiece)

        betsplit_ls = list(np.diff(np.array(index)))
        betsplit_ls.append(index[0])

        betsplit_ls = [x * self.min_betsize for x in betsplit_ls]

        print 'bet_split'
        print betsplit_ls
        # Sanity check before sharing
        if sum(betsplit_ls) != bet_amount:
            raise ValueError("sum(betsplit_ls) == bet_amount")

        # Find ghost most suitable, append them to a dataframe
        out_df = pd.DataFrame({'userid': [], 'telid': [], 'betquota': []})
        for bet in betsplit_ls:
            if bet > 0:
                userid, telid = self.find_most_suitable_ghost(bet, exclude_telid)
                tempdf = pd.DataFrame({'userid': [userid], 'telid': [telid], 'betquota': [bet]})
                out_df = out_df.append(tempdf)

                # Add exclusion
                exclude_telid.append(telid)

        return out_df

    def find_most_suitable_ghost(self, betsize, exclude_telid=[]):
        '''Function to search thru ghost_book and find most suitable ghost that would play this size, return TELID .
            Factors that affect which ghost:
                1) Current Time
                2) Size
            Different ghost has different appetite and might occur at different time etc

            @exclude_telid,  ghost to excluded (probably already on other mission)
        '''

        # Sanity check
        if betsize == 0:
            print "Betsize == 0"
            return None, None

        # Dictionary of ghost property
        curr_time = datetime.datetime.now().time()

        # Score each ghost (lower = better)
        score_dict = {}
        for index, g in self.ghost_book.iterrows():
            # Exclude if in this list
            if str(g['telid']) in exclude_telid:
                # print "Skipping this telid " + str(g['telid'])
                # print "Exclude list is "
                # print exclude_telid
                continue

            score = 0

            # If within working hour
            startHour = g['workhour_start']
            endHour = g['workhour_end']
            #if curr_time >= startHour and curr_time <= endHour:
            if True:
                score += 0
            else:
                score += 10

            # Sizes diff
            diff = abs(math.log(float(g['preferred_size'])) - math.log(betsize))
            score += diff

            # Add noise [-0.5, 0.5]
            # score += random.randrange(-50, 50) / 100
            score += random.randrange(-3, 3)

            # Save
            telid_key = str(g['telid'])
            if len(score_dict) == 0:
                score_dict = {telid_key: score}
            else:
                score_dict[telid_key] = score

        # Print score
        # for key in score_dict:
        #    print str(key) + " , " + str(score_dict[key])

        if len(score_dict) == 0:  # If got no candidate
            # raise ValueError('score_dict empty! ')
            print('score_dict empty! Ghostbook leng: ')
            print len(self.ghost_book)
            return None, None

        # Get min score telid
        best_candidiate_telid = str(min(score_dict, key=score_dict.get))

        # Get corresponding userid
        best_candidiate_userid = self.ghost_book.loc[self.ghost_book['telid'] == best_candidiate_telid]['userid']

        print "Best candidate telid: " + str(best_candidiate_telid) + "  for size: " + str(betsize)

        return best_candidiate_userid, best_candidiate_telid

    def deploy_ghost_to_server(self):
        """Main function to deploy ghost
        """
        # Extract the ghosts
        ghost_ups, ghost_downs = self.allocate_ghosts()

        # Place them into server
        num_ghost_deployed = 0
        if len(ghost_ups) > 0:
            for index, x in ghost_ups.iterrows():
                temp = bettingup.objects.filter(telid=x['telid'])
                if len(temp) == 0:
                    bettingup.objects.create(userid=x['userid'], telid=x['telid'], betquota=x['betquota'])
                    num_ghost_deployed += 1
                    print "bettingup ok: " + str(x.telid)
                else:
                    print "bettingup Already exists " + str(x.telid)

        if len(ghost_downs) > 0:
            for index, x in ghost_downs.iterrows():
                temp = bettingdwon.objects.filter(telid=x['telid'])
                if len(temp) == 0:
                    bettingdwon.objects.create(userid=x['userid'], telid=x['telid'], betquota=x['betquota'])
                    num_ghost_deployed += 1
                    print "bettingdwon ok: " + str(x.telid)
                else:
                    print "bettingdwon already exists " + str(x.telid)

        print "Ghost protocol done...ghost# planned:" + str(len(ghost_ups)) + "," + str(len(ghost_downs))
        print "Ghost# successfully deployed: " + str(num_ghost_deployed)


def Initialize_HappyHourProtocol():
    """Main Loop.
    Listen for server announcement, and deploy ghost bettor up/down """
    global HappyCheater

    # Before ghost protocol begins, create/get the users in SQL first. Fall
    ghost_book = init_users()
    print ghost_book

    has_deployed = False
    while True:  # A listener loop, to begin immediately 'Ghost Insertion' once gamesEnd
        time.sleep(0.5)

        # If at gamesStart stage, we may reset
        at_gamesStart = str(redisdb.ttl('gamesStart')) != "None"
        if has_deployed and at_gamesStart:
            has_deployed = False

        # If result is announced & and not yet deployed
        result_released = str(redisdb.ttl('gamesEnd')) != "None"
        if not has_deployed and result_released:
            print "Ghost Insertion begin: " + str(datetime.datetime.now().time())
            redisdb.set("GHOST_INSERTION", "ON")

            has_deployed = True
            # Peek into result shown in server
            time.sleep(1)  # wait 1 sec for server to be updated first
            netnumberdata = netnumber.objects.get(id=1)
            start_index = netnumberdata.fixednumber
            end_index = netnumberdata.finalnumber
            outcome = get_outcome(end_index, start_index)

            # Get current bettors that has placed their bet
            up_bettors, up_betsize, down_bettors, down_betsize = extract_real_bettors()

            if outcome == "UP":
                win_bet = sum(up_betsize)
                lose_bet = sum(down_betsize)
            elif outcome == "DOWN":
                win_bet = sum(down_betsize)
                lose_bet = sum(up_betsize)
            elif outcome == "DRAW": # Simply put as DOWN
                win_bet = sum(down_betsize)
                lose_bet = sum(up_betsize)

            # Create ghost, based on the bettors/outcome information
            print "the outcome is... " + outcome
            ghost_spawner = HappyCheater(outcome, win_bet, lose_bet, ghost_book)
            ghost_spawner.deploy_ghost_to_server()

            # End
            redisdb.delete("GHOST_INSERTION")
            print "End " + str(datetime.datetime.now().time())
            print "\n "


def createname(i):
    """
    Function to gen nick with suffix 100 "This is for ghost protocol"
    """
    numnunber = str(800000 + i) + "0000"
    return numnunber


def init_users(Npool=40):
    """Initialize users.
    Create if not exists in SQL, and return the DataFrame
    """
    # Npool Define total number of ghost


    # Define names
    nickname_list = []
    for i in range(0, Npool): # Get nickname from pool
        if i < len(nickname_pool):
            nickname_list.append(nickname_pool[i])

    # for the rest, just random generate number
    nickname_list += random.sample(range(100, 9999), max(0, Npool - len(nickname_list)))

    # Define telids
    telid_list = []
    for i in range(0, Npool):
        telid_list += ['Happyparty_0' + str(i)]

    # Define sizes
    preferred_sizes = [6000] * 10 + [2000] * 5 + [1000] * 10 + [500] * 5
    preferred_sizes += [200] * max(0, Npool - len(preferred_sizes))

    # Define working hour
    start_vec = []
    end_vec = []
    for i in range(0, Npool):
        # Randomly set start hour and end hour
        start_hour = random.randint(0, 23)
        start_vec.append(start_hour)

        # End hour = StartHour + random workhour
        end_hour = start_hour + random.randint(1, 5)
        end_hour = end_hour % 24
        end_vec.append(end_hour)

    # Create user in SQL
    userid_list = []
    for i in range(0, Npool):
        nickname = nickname_list[i]
        telid = telid_list[i]

        if is_user_exist(telid):
            user = Extend_user.objects.get(telid=telid)
            userid_list.append(user.ext_user_id)
            print "User " + str(telid) + " exist."
            pass
        else:
            # Create
            print "Happyparty protocol " + str(telid)
            password = random.randint(10000, 99999)
            name = createname(i)

            creatuser = User.objects.create_user(username=name, password=str(password))
            Extend_user.objects.get_or_create(ext_user_id=creatuser.id,
                                                      username=str(name),
                                                      pawword=password,
                                                      telid=telid,
                                                      openid=str(name) + '_aa',
                                                      xcoin=1000000,
                                                      btcaddress=str(name) + '_no',
                                                      giveusermoney=300,
                                                      notice='大家好',
                                                      isreferee=False,
                                                      userisrun=False,
                                                    screen_name=nickname,)
            userid_list.append(creatuser.id)
            print "User " + str(telid) + " created."


    # Create Dataframe and return
    user_list = pd.DataFrame({'userid': userid_list,
                               'username': nickname_list,
                               'telid': telid_list,
                               'preferred_size': preferred_sizes,
                               'workhour_start': start_vec,
                               'workhour_end': end_vec})
    return user_list


def is_user_exist(telid):
    exist_count = Extend_user.objects.filter(telid=telid).count()

    if exist_count >= 1:
        return True
    else:
        return False


def extract_real_bettors():
    """Get current bettors from SQL that has placed their bet.
        return 4 different list of
        [up_bettors, up_betsize, down_bettors, down_betsize]
    """
    down_bettors = []
    down_betsize = []
    betdownManager = bettingdwon.objects.all()
    for betdownObj in betdownManager:
        down_bettors.append(betdownObj.userid)
        down_betsize.append(betdownObj.betquota)

    up_bettors = []
    up_betsize = []
    betupManager = bettingup.objects.all()
    for betupObj in betupManager:
        up_bettors.append(betupObj.userid)
        up_betsize.append(betupObj.betquota)

    return up_bettors, up_betsize, down_bettors, down_betsize


def get_outcome(end_index, start_index):
    """Return UP DOWN or DRAW """
    if end_index > start_index:
        return "UP"
    elif end_index < start_index:
        return "DOWN"
    elif end_index == start_index:
        return "DRAW"
    else:
        return 0

nickname_pool = [
            '源子',
            '因循小暑来',
            '怪老牛hehe',
            '公私合营',
            '华海',
            '阿德寿',
            '任浩广999',
            '海小蕊133',
            '贝亦巧',
            '梁丘秋颖',
            '东方映寒留',
            '静娴寒灵萱',
            '初沛容1660',
            '华清尔',
            '清佳昔绮',
            '怀犁伟泽1988',
            '曾嘉玉军',
            '小萍',
            '张简娟',
            '叶欣学bob',
            '夏之剑',
            '~从筠尚奇文暴~',
            '初夏万俟',
            '咸英Swift',
            '问芸若',
            '~~俞莹玉~~',
            '**欧阳唱月**',
            '[佼芳春]',
            '*钭芳泽*',
            '*章晗蕊声之桃*',
            '~~ 司空和蔼 ~~',
            '潜晴1221',
            '雪陆',
            '清秋甄白',
            '云蛮岚',
            'Power Ranger',
            '脑残经'
            'Ayako'
]

if __name__ == '__main__':
    redisdb.delete("GHOST_INSERTION")
    Initialize_HappyHourProtocol()
