from django.utils import timezone
import pytz
if __name__ == '__main__':
    # Run only once. Dont keep running
    # 这里是创建300个假用户.执行一次就可以.
    # for ind in xrange(0, 300):
    #  cuser()

    # Get the current index
    start_index = 6300.00

    ###################################
    # Listen for bet from player
    ###################################
    # Model fake betting
    userid_list = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7"]

    # Reset all
    # bettingup.objects.all().delete()
    for test_telid in userid_list:
        # Get user information
        x = Extend_user.objects.get(ext_user_id=test_telid)

        # Simulate time
        timezone.now()
        bet_time = datetime.datetime(2018, 7, 18, 5, 13, 21, tzinfo=pytz.timezone('Asia/Shanghai'))

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
                print str(bettor.telid) + " top up bet"
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
                print str(bettor.telid) + " top up bet"
            else:
                # Create entry
                bettingdwon.objects.get_or_create(userid=x.id, telid=x.telid, betquota=bet_size, bettime=bet_time)

        print x.telid + " bet " + str(bet_size) + " On up: " + str(bet_isUp)


    ###################################
    # Aggregate Result
    ###################################
    # Get result
    end_index = 6500.00

    # Allocate reward
    allocator = BetAllocation(start_index, end_index, up_bettor_ids, up_bets, down_bettor_ids, down_bets)
    allocator.AllocatePoint()
    
    print "Program end"

import NumPy as pd
from enum import Enum     # for enum34, or the stdlib version
class BetAllocation:
    """Perform win/lose Allocation"""
    # All possible outcome
    Outcome = Enum("UP", "DOWN", "EQUAL")
    
    # reward ratio for winner. I.e. winner bet 100, loser bet 500, ratio = 5
    win_ratio
    
    # Data frame of ID/Bet size
    up_bettors
    down_bettors
    
    def __init__(self):
        self.data = []
        
    def __init__(self, start_index, end_index, up_bettor_ids, up_bets, down_bettor_ids, down_bets):
        
        # Create DataFrame
        self.up_bettors = CreateDF(up_bettor_ids, up_bets)
        self.down_bettors = CreateDF(down_bettor_ids, down_bets)
        
        # Decide outcome
        self.Outcome = GetOutcome(start_index, end_index)
        
        # Compute ratio
        self.Outcome

    
    def CreateDF(ids, bets):
        """Function to create and return list of data.frame
        """
        if len(ids) != len(bets):
            raise ValueError("len(ids) != len(bets)")
            
        return pd.DataFrame(user_id=userid, betsize=bets)

    
    def GetOutcome(start_index, end_index):
        """Compare index and provide outcome"""
        try:
            if(end_index > start_index):
                return Enum.UP
            else if(end_index < start_index):
                return Enum.DOWN
            else if(end_index == start_index):
                return Enum.EQUAL
            else
                raise ValueError('Unknown outcome. Start_index and end_index compared but no outcome')
        except:
            raise ValueError('Unknown outcome. Start_index and end_index not comparable')


    def GetWinners():
        """Return DataFrame of winners"""
        if Outcome == Enum.UP:
            return up_bettors
        else if Outcome == Enum.DOWN:
            return down_bettors
        else if Outcome == Enum.EQUAL:
            return []   #TODO:
        else:
            raise TransitionError('Unknown outcome. not sure who is winners')
           
           
    def GetLosers():
        """Return DataFrame of losers"""
        if Outcome == Enum.UP:
            return down_bettors
        else if Outcome == Enum.DOWN:
            return up_bettors
        else if Outcome == Enum.EQUAL:
            return []   #TODO:
        else:
            raise TransitionError('Unknown outcome. not sure who is winners')


    def GetTotalRewardBeforeFee():
        """Reward = Compute total bet put by losers. Return a numeric """
        loserdf = GetLosers()
        return userdf['betsize'].sum()
    
    
    def ComputeRatio():
        """ 
        Function to compute Ratio and define fees.
        Define Fee formula here. The better the ratio, the more the fee 
        """
        # Compute Ratio first
        losers_df = GetLosers()
        winners_df = GetWinners()
        win_ratio = losers_df.sum()/winners_df = GetWinners()
    
      
    def ComputeFee(ratio):
        """ 
        Define Fee formula here. The better the ratio, the more the fee 
        """
        if ratio > 100:
            fee = 0.15
        else if ratio > 50:
            fee = 0.10
        else if ratio > 10:
            fee = 0.08
        else if ratio > 2:
            fee = 0.05
        else if ratio > 0.9:
            fee = 0.05
        else if ratio > 0.5:
            fee = 0.05
        else
            fee = 0.025
        return fee
     
     
    # TOOD: If draw, think about it
    def AllocatePoint():
        """ Main function to compute and allocate points """
        totalreward_before_fee = GetTotalRewardBeforeFee()
        
        ComputeRatio()
        
        fee = ComputeFee(win_ratio) 
        
        totalreward_after_fee = totalreward_before_fee * (1 - fee)
        
        
        # Distribute the reward according to relative weight
        winners_df = GetWinners()
        total_weight = winners_df['betsize'].sum()
        winners_relative_weight = winners_df['betsize'] / total_weight
        individual_reward = totalreward_after_fee * winners_relative_weight
        
        # save to server
        
           
