import random
import pandas

has_deployed = False


def Initialize_GhostProtocol():
    """Listen for server announcement, and deploy ghost bettor up/down """
    while True:
		# If at Game_End stage, we may reset
		at_gamesEnd = str(redisdb.get('gamesEnd')) == "end"
		if has_deployed and at_gamesEnd:
			has_deployed = False
		
        # If result is announced & and not yet deployed
        result_released = str(redisdb.get('gamesYeid')) == "yes"
        if not has_deployed and result_released:
            has_deployed = True

            # Peek into result shown in server
            netnumberdata = netnumber.objects.get(id=1)
            start_index = netnumberdata.fixednumber
            end_index = netnumberdata.finalnumber
            outcome = get_outcome(end_index, start_index):

            # Get current bettors that has placed their bet
			up_bettors, up_betsize, down_bettors, down_betsize = extract_bettors()

			if outcome == "UP":
				win_bet = up_betsize.sum()
				lose_bet = down_betsize.sum()
			elif outcome == "DOWN":
				win_bet = down_betsize.sum()
				lose_bet = up_betsize.sum()

			# Create ghost, based on the bettors/outcome information
			ghost_spawner = Cheater(outcome, win_bet, lose_bet, num_winners, num_losers)
			ghost_spawner.deploy_ghost_to_server()

			
def extract_bettors():
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
	else
		return 0


class Cheater:
    outcome = []
    win_bet = []
    lose_bet = []
    num_winners = 0
    num_losers = 0
    min_betsize = 100.0
	ghost_book = []

    def __init__(self):
        self.data = []

    def Cheater(self, outcome, win_bet, lose_bet, num_winners, num_losers):
        self.outcome = outcome
        self.win_bet = win_bet
        self.lose_bet = lose_bet
        self.num_winners = num_winners
        self.num_losers = num_losers
		
		# TODO: Example 
		for i in range(0, 5):
			curr_time = datetime.datetime.now().time()
			a = pd.DataFrame({'userid': [i], 'telid': [123*i], 'preferred_size': [i*100+100], 'workhour_start': [curr_time], 'workhour_end': [curr_time]})
			self.ghost_book = self.ghost_book.append(a)
			

    def get_min_winlose_size():
        """Get the optimal win/lose bet according to Golden Ratio
        """
        adj_lose_bet = min_betsize
        adj_win_bet = Math.ceil(adj_lose_bet * self.win_bet / self.lose_bet)

        return adj_win_bet, adj_lose_bet

    def allocate_ghosts():
        """ Return ghosts and with bet size that will satisfy Golden Rule
		Return two dataframes, one for up-side ghost, one for down side
        Dataframe is in (userid, telid, bet_size).		
        """
        min_bet_win, min_bet_lose = get_min_winlose_size()

        # Increase the winning size such that it is at least integer of lose bet
        min_bet_win = ceil(min_bet_win / min_bet_lose) * min_bet_lose

        # Randomize
        num_lost_ghost = rand.range(1, 3)

        # Scale up by
        bet_lose = num_lost_ghost * min_bet_lose
        bet_win = num_lost_ghost * min_bet_win

        # Create ghost characteristic
        losers_df = split_bet_across(bet_lose, num_lost_ghost)

        num_win_ghost = rand.range(1, 3)
        winners_df = split_bet_across(bet_win, num_win_ghost)

        # Convert to up/down
        if self.outcome == Outcome.UP
            ghost_up_df = winners_df
            ghost_down_df = losers_df
        elif self.outcome == Outcome.DOWN
            ghost_up_df = losers_df
            ghost_down_df = winners_df

        return ghost_up_df, ghost_down_df

		
	def split_bet_across(bet_amount, N):
		"""Split bets across different ghosts.
		Ensure each bet follow multiple of min_size
		return DataFrame
		"""		
		# Sanity check
		if round(bet_amount / min_size) - (bet_amount / min_size) > 0.00001:
			raise ValueError("bet_amount not multiple of bet_amount")
		else:
			npiece = bet_amount / min_size
		
		# Split the piece
		x = range(0, npiece)
		index = random.sample(x, n - 1)
		index = sorted(index)
		index.append(npiece)

		betsplit_ls = list(np.diff(np.array(index)))
		betsplit_ls.append(index[0])
		
		betsplit_ls = [x * 100 for x in betsplit_ls]
		
		# Sanity check before sharing
		if sum(betsplit_ls) == bet_amount:
			return betsplit_ls
		else:
			raise ValueError("sum(betsplit_ls) == bet_amount")
			
		# Find ghost most suitable, append them to a dataframe
		out_df = pd.DataFrame({'userid': [], 'telid': [], 'betquota': []})
		for bet in betsplit_ls:
			userid, telid  = find_most_suitable_ghost(bet)
			tempdf = pd.DataFrame({'userid': [userid], 'telid': [telid], 'betquota': [bet]})
			out_df = out_df.append(tempdf)
			
		return out_df
		
		
	def find_most_suitable_ghost(betsize):
		'''Function to search thru ghost_book and find most suitable ghost that would play this size, return TELID .
			Factors that affect which ghost:
				1) Current Time
				2) Size
			Different ghost has different appetite and might occur at different time etc
		'''
		# TODO: 
		# Before ghost protocol begins, create/get the users in SQL first. Fall
		# ghost_book = pd.DataFrame({'userid': [], 'telid': [], 'preferred_size': [], 'workhour_start': [], 'workhour_end': []})
		
		# Dictionary of ghost property
		curr_time = datetime.datetime.now().time()
		
		# Score each ghost (lower = better)
		score_dict = {'EMPTY': 100000000000}
		for index, g in ghost_book.iterrows():
			score = 0
			
			print g
			# If within working hour
			startHour = g['workhour_start']
			endHour = g['workhour_end']
			if curr_time >= startHour and curr_time <= endHour:
				score += 0
			else:
				score += 10
			
			# If match sizes
			diff = abs(math.log(float(g['preferred_size'])) - math.log(betsize))
			score += diff
			
			# Save
			telid_key = str(g['telid'])
			if len(score_dict) == 0:
				#score_dict = dict(telid_key=score)
				#score_dict = {g, score}
				score_dict = {telid_key: score}
			else:
				score_dict[telid_key] = score
			
		# Get min score telid
		best_candidiate_telid = str(min(score_dict, key=score_dict.get))

		return best_candidiate_telid
		

    def deploy_ghost_to_server():
		# Extract the ghosts
        ghost_ups, ghost_downs = allocate_ghosts()

		# Place them into server
        for x in ghost_ups:
            temp = bettingup.objects.filter(telid=x.telid)
            if temp.count() == 0:
                bettingup.objects.create(userid=x.userid, telid=x.telid, betquota=x.betquota)

        for x in ghost_downs:
            temp = bettingdwon.objects.filter(telid=x.telid)
            if temp.count() == 0:
                bettingdwon.objects.create(userid=x.userid, telid=x.telid, betquota=x.betquota)

        print "Ghost protocol done...g:" + str(ghost_ups.count() + ghost_downs.count())
