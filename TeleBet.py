####################################
# Gambling bot
####################################
/Start
	-> Display Button Bet Size	[Wait user click]
			[1]		[2]		[5]
			[10]	[50]	[100]
			[500]	[....	]
	-> Display Button for 
			[Up] 	[Down]
	-> Display Button for 
			Bet Up for 100b
			[back] 	[Submit]		
		[Wait user click]
	-> send msg "/Bet up 100"
	
# Function to place bet 
/Bet arg1 arg2
	arg1, 	bet outcome 
	arg2,	bet size

# Display current index
/showindex

# Show past historical outcome
/pastresult 20
	arg1, how many result to show


####################################
# Result aggregator bot
####################################
[str,int] upUsers
[str,int] downUsers
float currentIndex
float resultIndex
roundInfo roundInfo

@print_team
List out upUsers and their bet
List out downUsers and their bet

@print_winners(up)
List out only winners team

@total_bet(outcome)
Get total bet of up

@roundInfo class
	StartTime 	(in date and time)
	EndTime		(in date and time)
	startPoint
	endPoint

@Reconcile_Bet()
#  get resultIndex,
resultIndex = ShowIndex()

if resultIndex > currentIndex
	Outcome = UP
else if resultIndex < currentIndex
	Outcome = DOWN
else #Draw ! 
	Outcome = DRAW

# IF DRAW, MOVE TO SPECIAL MOMENT


#  get current win payout ratio
if Outcome == UP
	ratio = total_bet(Down)/total_bet(UP)
else if Outcome == Down
	ratio = total_bet(UP)/total_bet(Down)

# get fee percentage
if ratio > 100
	fee = 0.15
else if ratio > 50
	fee = 0.10
else if ratio > 10
	fee = 0.08
else if ratio > 2
	fee = 0.05
else if ratio > 0.9
	fee = 0.05
else if	ratio > 0.5
	fee = 0.05
else
	fee = 0.025

draw_fee = 0.05
	
# reallocate losers point to winners 
if Outcome == UP
	winners = upUsers
	losers = downUsers
else if Outcome == Down
	winners = downUsers
	losers = upUsers
else if Outcome == DRAW
	winners = upUsers
	winners.Add(downUsers)
else if Outcome == UN_RESOLVED 	# everyone lose
	losers = upUsers
	losers.Add(downUsers)

########## UP/DOWN situation ##########	

# Ask server to update points, send msg to all of them
for(user in winners)
	payout = betsize[user] * ratio * (1-fee)

	PostServer(user, payout, roundInfo, outcome)
	SendWinnerMsg(user, payout, roundInfo, outcome)

for(user in losers)
	PostServer(user, roundInfo, outcome)
	SendLoserMsg(user, roundInfo, outcome)

	
@SendWinnerMsg(user, payout, roundInfo, outcome, )
	.SendMSG(user, "Bet# " + roundInfo, " You bet " + betDir + " for $" + betsize[user])
	.SendMSG(user, " You win" + payout + ".")

		
@SendLoserMsg(user, roundInfo, outcome, )
	.SendMSG(user, "Bet# " + roundInfo, " You bet " + betDir + " for $" + betsize[user])
	.SendMSG(user, " You lose")

