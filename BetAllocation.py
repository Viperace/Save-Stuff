# -*- coding: utf-8 -*-

# ***** django requirement *******
import sys
import os
import platform
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


# ***** My class *******
import pandas as pd
from pandas import Series
from enum import Enum
from btchtm.models import bettingup, bettingdwon, Extend_user, winning, whistory #winnersAndLosers banker_history
#from django.utils import timezone
import pytz
import datetime
from datetime import timedelta
import random



class Outcome(Enum):
    """Define all possible outcome """
    WAITING = 0
    UP = 1
    DOWN = 2
    EQUAL = 3
    IMBALANCE = 4


class BetManager:
    """Judge, decide who wins, who lose. Decide how much winner takes"""
    # Outcome
    current_outcome = Outcome.WAITING

    # reward ratio for winner. I.e. winner bet 100, loser bet 500, ratio = 5
    up_down_ratio = []

    # Data frame of ID/Bet size
    up_bettors = []
    down_bettors = []

    def __init__(self):
        self.data = []

    def __init__(self, up_bettor_ids, up_bets, up_bettime, down_bettor_ids, down_bets, down_bettime):
        # Create DataFrame
        self.up_bettors = self.CreateDF(up_bettor_ids, up_bets, up_bettime)
        self.down_bettors = self.CreateDF(down_bettor_ids, down_bets, down_bettime)

        # Compute ratio
        self.up_down_ratio = self.ComputeRatio()

    #def __init__(self, start_index, end_index, up_bettor_ids, up_bets, up_bettime,
    #             down_bettor_ids, down_bets, down_bettime):
    #    # Create DataFrame
    #    self.up_bettors = self.CreateDF(up_bettor_ids, up_bets, up_bettime)
    #    self.down_bettors = self.CreateDF(down_bettor_ids, down_bets, down_bettime)

        # Decide outcome
        #self.current_outcome = self.GetOutcome(start_index, end_index,
        #                                       len(self.up_bettors), len(self.down_bettors))

        # Compute ratio
        #self.up_down_ratio = self.ComputeRatio()

    def CreateDF(self, ids, bets, times):
        """Function to create and return list of data.frame
        """
        if len(ids) != len(bets):
            raise ValueError("len(ids) != len(bets)")

        if len(ids) != len(times):
            raise ValueError("len(ids) != len(times)")

        return pd.DataFrame({'user_id': ids, 'betSize': bets, 'bet_time': times})

    def GetOutcome(self, start_index, end_index, num_up, num_down):
        """Compare index and provide outcome"""
        # Check for imbalance first
        if num_up == 0 or num_down == 0:
            return Outcome.IMBALANCE

        try:
            # Check for others
            if end_index > start_index:
                return Outcome.UP
            elif end_index < start_index:
                return Outcome.DOWN
            elif end_index == start_index:
                return Outcome.EQUAL
            else:
                raise ValueError('Unknown outcome. Start_index and end_index compared but no outcome')
        except:
            raise ValueError('Unknown outcome. Start_index and end_index not comparable')

    def GetWinners(self):
        """Return DataFrame of USER_ID / BETSIZE of winners"""
        if self.current_outcome == Outcome.UP:
            return self.up_bettors
        elif self.current_outcome == Outcome.DOWN:
            return self.down_bettors
        elif self.current_outcome == Outcome.EQUAL:
            return []
        elif self.current_outcome == Outcome.IMBALANCE:
            return []
        elif self.current_outcome == Outcome.WAITING:
            return []
        else:
            raise ValueError('Unknown outcome. not sure who is winners')

    def GetLosers(self):
        """Return DataFrame of  USER_ID / BETSIZE of losers"""
        if self.current_outcome == Outcome.UP:
            return self.down_bettors
        elif self.current_outcome == Outcome.DOWN:
            return self.up_bettors
        elif self.current_outcome == Outcome.EQUAL:
            return []
        elif self.current_outcome == Outcome.IMBALANCE:
            return []
        elif self.current_outcome == Outcome.WAITING:
            return []
        else:
            raise ValueError('Unknown outcome. not sure who is winners')

    def GetTotalRewardBeforeFee(self):
        """Reward = Compute total bet put by losers. Return a numeric """
        loser_df = self.GetLosers()
        return loser_df['betSize'].sum()

    def ComputeRatio(self):
        """
        Function to compute Ratio of UP_sum/DOWN_sum.
        Return 0 if any one side has no bettor
        """
        # Compute Ratio first
        if len(self.up_bettors) == 0:
            return 0
        elif len(self.down_bettors) == 0:
            return 0
        else:
            return 1.0 * self.up_bettors['betSize'].sum() / self.down_bettors['betSize'].sum()

    @staticmethod
    def ComputeFee(ratio):
        """
        赢得越大，抽成越大
        Define Fee formula here. The better the ratio, the more the fee
        """
        if ratio > 100:
            return 0.10
        elif ratio > 10:
            return 0.05
        elif ratio > 2:
            return 0.05
        elif ratio > 0.9:
            return 0.03
        else:
            return 0.03

    def AllocatePoint(self, announce_time, start_index, end_index):
        """ Main function to compute and allocate points """

        # Resolve Outcome first
        self.current_outcome = self.GetOutcome(start_index, end_index,
                                               len(self.up_bettors), len(self.down_bettors))

        # Allocate point
        if self.current_outcome == Outcome.EQUAL or self.current_outcome == Outcome.IMBALANCE:
            self.ReturnAllBets()

            # Save announcement result
            winning.objects.all().delete()  # Reset
            # total_bet = self.up_bettors['betSize'].sum() + self.down_bettors['betSize'].sum()

            total_bet = 0
            if len(self.up_bettors) > 0:
                total_bet += self.up_bettors['betSize'].sum()
            if len(self.down_bettors) > 0:
                total_bet += self.down_bettors['betSize'].sum()

            winning.objects.create(userup=len(self.up_bettors['betSize']),
                                   userdown=len(self.down_bettors['betSize']),
                                   theodds=0,
                                   quota=total_bet)
            winning.save()

            # TODO: Save banker's history
            #banker_history.objects.create(the_odds=0, fee=0, fee_size=0, bettime=announce_time)
        else:
            # Get basic information
            total_reward = self.GetTotalRewardBeforeFee()

            self.up_down_ratio = self.ComputeRatio()
            if self.current_outcome == Outcome.UP:
                win_ratio = 1.0 / self.up_down_ratio
            else:
                win_ratio = self.up_down_ratio

            fee = self.ComputeFee(win_ratio)

            winners_df = self.GetWinners()
            losers_df = self.GetLosers()

            total_bet = winners_df['betSize'].sum() + losers_df['betSize'].sum()

            # Output
            print str(announce_time) + " 开： " + str(self.current_outcome)
            print "win_ratio: " + str(win_ratio)
            print "Fee: " + str(fee)
            print "Fee Amount: " + str(total_reward * fee)
            print "winners: "
            print winners_df
            print "losers: "
            print losers_df

            # Compute winner's share (after fee and rounding)
            # 赢家收回= 本金 + 胜利额
            #   胜利额 = ROUND[ 本金*（1 - 抽成） ]
            reward = winners_df['betSize'] * win_ratio * (1 - fee)
            coinsToAdd = Series.round(reward) + winners_df['betSize']
            print "Money to payback: " + str(coinsToAdd)

            # Save announcement result
            winning.objects.all().delete()  # Reset
            winning.objects.create(userup=len(self.up_bettors['betSize']),
                                   userdown=len(self.down_bettors['betSize']),
                                   theodds=win_ratio,
                                   quota=total_bet)
            winning.save()

            # Request server to re-allocate xcoin
            RewardAllocator(winners_df['user_id'], coinsToAdd)

            #------- 记录而已 ------------
            # TODO: Update winning list
            #winnersAndLosers.objects.all().delete()  # Reset
            for i in range(0, len(winners_df)):
                #bet_size = round(winners_df.iloc[i]['betSize'])
                user_id = winners_df.iloc[i]['user_id']
                #winnersAndLosers.objects.create(winners_list=user_id)

            for i in range(0, len(losers_df)):
                #bet_size = round(losers_df.iloc[i]['betSize'])
                user_id = losers_df.iloc[i]['user_id']
                #winnersAndLosers.objects.create(losers_list=user_id)

            # Save winner's history
            # TODO: Do faster loop
            for i in range(0, len(winners_df)):
                win_size = coinsToAdd[i]
                user_id = winners_df.iloc[i]['user_id']
                #bet_time = winners_df.iloc[i]['bet_time']
                whistory.objects.create(userid=user_id, quota=win_size, bettime=announce_time)

            # TODO: Save banker's history
            #banker_history.objects.create(fee=fee, fee_size=round(total_reward * fee, 0), the_odds=self.win_ratio,
            #                              bettime=announce_time)



    def ReturnAllBets(self):
        """Function to loop through all bettor and return their bet"""
        print "ReturnAllBets"
        for i in range(0, len(self.up_bettors)):
            user_id = self.up_bettors.iloc[i]['user_id']
            bet_size = self.up_bettors.iloc[i]['betSize']
            user = Extend_user.objects.get(ext_user_id=user_id)
            user.xcoin += bet_size
            user.save()

        for i in range(0, len(self.down_bettors)):
            user_id = self.down_bettors.iloc[i]['user_id']
            bet_size = self.down_bettors.iloc[i]['betSize']
            user = Extend_user.objects.get(ext_user_id=user_id)
            user.xcoin += bet_size
            user.save()



class RewardAllocator:
    """Ask server to update points for winner and losers"""
    winners_df = []

    def __init__(self):
        self.data = []

    def __init__(self, winners, coins_to_add):

        # Sanity check
        if len(winners) != len(coins_to_add):
            raise ValueError('winners_df length must be equal to coins_to_add')

        self.winners_df = pd.DataFrame({'user_id': winners, 'coin_to_add': coins_to_add})

        # Loop thru each winner, and add winning coin
        for i in range(0, len(self.winners_df)):
            winner_id = self.winners_df.iloc[i]['user_id']
            winner_newcoin = self.winners_df.iloc[i]['coin_to_add']

            winner = Extend_user.objects.get(ext_user_id=winner_id)
            winner.xcoin += winner_newcoin
            winner.save()


def BetPlacementSimulation(numuser=7):
    ###################################
    # Listen for bet from player
    ###################################
    # Init (clear at the end too, this is extra
    bettingup.objects.all().delete()
    bettingdwon.objects.all().delete()
    #winnersAndLosers.objects.all().delete()

    # Simulate getting the current index
    start_index = 6300.00

    # 随机抽出N个用户来模拟
    # Simulate list of users that perform the betting
    userid_list = random.sample(range(1, 300), numuser)
    #userid_list = ["1", "2", "3", "4", "5", "6", "7"]

    # Simulate each user's bet
    for i in xrange(0, 1):
        for test_telid in userid_list:
            # Get user information
            x = Extend_user.objects.get(ext_user_id=test_telid)

            # Simulate time
            # timezone.now()
            # bet_time = datetime.datetime(2018, 7, 18, 5, 13, 21, tzinfo=pytz.timezone('Asia/Shanghai'))
            bet_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
            eps = random.randint(0, 150)*1000
            bet_time += timedelta(seconds=eps)

            # Simulate size
            bet_size = random.randint(20, 50) * 10

            # Simulate direction
            bet_isUp = random.randint(0, 100) > 50

            # Simulate place bet
            if bet_isUp:
                existing_bettor = bettingup.objects.filter(userid=test_telid)

                # If existing, then topup
                if existing_bettor.count() > 0:
                    bettor = bettingup.objects.get(userid=test_telid)
                    bettor.betquota += bet_size  # Add more !
                    bettor.save()
                    print str(bettor.userid) + " / " + str(bettor.telid) + " top up bet"
                else:
                    # Create entry
                    bettingup.objects.get_or_create(userid=x.id, telid=x.telid, betquota=bet_size, bettime=bet_time)
            else:
                existing_bettor = bettingdwon.objects.filter(userid=test_telid)

                # If existing, then topup
                if existing_bettor.count() > 0:
                    bettor = bettingdwon.objects.get(userid=test_telid)
                    bettor.betquota += bet_size  # Add more !
                    bettor.save()
                    print str(bettor.userid) + " / " + str(bettor.telid) + " top up bet"
                else:
                    # Create entry
                    bettingdwon.objects.get_or_create(userid=x.id, telid=x.telid, betquota=bet_size, bettime=bet_time)

            print str(x.ext_user_id) + " / " + str(x.telid) + " bet " + str(bet_size) + " On up: " + str(bet_isUp)

    ###################################
    # Aggregate Result
    ###################################
    # Simulate Get result
    end_index = start_index + random.randrange(-10, 10)

    # Simulate announce time
    announce_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))

    # Allocate reward

    # Extract up bettor
    down_bettors = bettingdwon.objects.values_list('userid', flat=True)
    down_betsize = bettingdwon.objects.values_list('betquota', flat=True)
    down_bettime = bettingdwon.objects.values_list('bettime', flat=True)

    up_bettors = bettingup.objects.values_list('userid', flat=True)
    up_betsize = bettingup.objects.values_list('betquota', flat=True)
    up_bettime = bettingup.objects.values_list('bettime', flat=True)

    # Check winner/loser and allocate points
    betManager = BetManager(up_bettors, up_betsize, up_bettime,
                            down_bettors, down_betsize, down_bettime)

    betManager.AllocatePoint(announce_time, start_index, end_index)
