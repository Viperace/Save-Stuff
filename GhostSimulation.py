has_deployed = False


def Initialize_GhostProtocol():
    """Listen for server annoucnement, and deploy bettor up/down """
    while True:
        # If result is announced
        result_released = str(redisdb.get('gamesYeid')) == "yes"
        if not has_deployed and result_released:
            has_deployed = True

            # Get result
            netnumberdata = netnumber.objects.get(id=1)
            start_index = netnumberdata.fixednumber
            end_index = netnumberdata.finalnumber
            outcome = get_outcome(end_index, start_index):

            # Get current bettors
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

                if outcome == "UP":
                    win_bet = up_betsize.sum()
                    lose_bet = down_betsize.sum()
                elif outcome == "DOWN":
                    win_bet = down_betsize.sum()
                    lose_bet = up_betsize.sum()

                # Create
                ghost_spawner = Cheater(outcome, win_bet, lose_bet, num_winners, num_losers)
                ghost_spawner.deploy_ghost_to_server()


                # If at Game_End stage, we may reset
    at_gamesEnd = str(redisdb.get('gamesEnd')) == "end"
    if has_deployed and at_gamesEnd:
        has_deployed = False

    def get_outcome(end_index, start_index):
        if end_index > start_index:
            return "UP"
        elif end_index < start_index:
            return "DOWN"
        elif end_index == start_index:
            return "DRAW"
        else
            return 0


class Cheater:
    outcome = []
    win_bet = []
    lose_bet = []
    num_winners = 0
    num_losers = 0
    min_betsize = 100.0


    def __init__(self):
        self.data = []


    def Cheater(self, outcome, win_bet, lose_bet, num_winners, num_losers):
        self.outcome = outcome
        self.win_bet = win_bet
        self.lose_bet = lose_bet
        self.num_winners = num_winners
        self.num_losers = num_losers

    def get_min_winlose_size():
        """Get the optimal win/lose bet according to Golden Ratio
        """
        bet_on_lose = min_betsize
        bet_to_win = Math.ceil(bet_on_lose * self.win_bet / self.lose_bet)

        return bet_to_win, bet_on_lose

    def allocate_ghosts():
        """ Return two dataframes, one for up-side ghost, one for down side
        Dataframe is in (userid, telid, bet_size)
        """
        min_bet_win, min_bet_lose = get_min_winlose_size()

        # Make the winning side always integer
        min_bet_win = ceil(min_bet_win / min_bet_lose) * min_bet_lose

        # Randomize
        num_lost_ghost = rand.range(1, 3)

        # Scale up by
        bet_lose = num_lost_ghost * min_bet_lose
        bet_win = num_lost_ghost * min_bet_win

        # Create ghost characteristic
        losers_df = suggest_split(bet_lose, num_lost_ghost)

        num_win_ghost = rand.range(1, 3)
        winners_df = suggest_split(bet_win, num_win_ghost)

        # Convert to up/down
        if self.outcome == Outcome.UP
            ghost_up_df = winners_df
            ghost_down_df = losers_df
        elif self.outcome == Outcome.DOWN
            ghost_up_df = losers_df
            ghost_down_df = winners_df

        return ghost_up_df, ghost_down_df


    def deploy_ghost_to_server():
        ghost_ups, ghost_downs = allocate_ghosts()

        for x in ghost_ups:
            temp = bettingup.objects.filter(telid=x.telid)
            if temp.count() == 0:
                bettingup.objects.create(userid=x.userid, telid=x.telid, betquota=x.betquota)

        for x in ghost_downs:
            temp = bettingdwon.objects.filter(telid=x.telid)
            if temp.count() == 0:
                bettingdwon.objects.create(userid=x.userid, telid=x.telid, betquota=x.betquota)

        print "Ghost protocol done...g:" + str(ghost_ups.count() + ghost_downs.count())
