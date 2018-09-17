upid_get_reward = 0, 1, 2
	0: Initialized, Unclaimable
	1: Claimable
	2: Already claimed
	
0: Init is this
1: Check for '0' status,
	If downline user payhistory, sum of total value is > 1000, then set to '1'
	Allow claim of 50

2: Check for '1' status,
	If user has claimed, then change to '2'

def claim_reward(bot, update, telid):
    """
    Process to give all unclaimed reward to user, send a message telling him that.
    Search through SQL up_id for all unclaimed reward, send one lump-sum to the user, and reset the indicators

    User must top-up at least 2000 x-coin, in order for upid user to gain reward 100 xcoin
	
	upid_get_reward = 0, 1, 2
		0: Initialized, Unclaimable
		1: Claimable
		2: Already claimed
    """
	from pay.models import Payhistory
	
	topup_threshold = 2000  # Amount a downline user need to topup for up user to be eligible for reward
	reward_size = 100		# Reward amount for each downline user success
    query = update.callback_query

    # Check all pending reward belong to this user
    userid = get_userid_from_telid(telid)
    user_downline_data = up_id.objects.filter(upid=userid)

    # Loop each of this user's downline, and check if they have satisfied top-up condition
	# 
    total_new_friends = 0
	total_reward = 0
    for down_user in user_downline_data:
		# To check if top-up condition reached, update indicator if it is
        if down_user.upid_get_reward == 0:  
            # Check this user_id's topup history
			topup_history = Payhistory.objects.filter(userid=down_user.userid)
			if len(topup_history) > 0:
				# Get total x-coin topup
				topup_amount = topup_history.aggregate(Sum('value'))/100	
				
				# Condition reached, set indicator
				if topup_amount > topup_threshold:			
					down_user.upid_get_reward = 1
					down_user.save()
		
		# To check if redeemable, redeem if it is
		if down_user.upid_get_reward == 1:
			# Update total reward to give
            total_new_friends += 1
			total_reward += reward_size
			
			# Save sql
			down_user.upid_get_reward = 2
            down_user.save()
            

    # Give rewards to user
    if total_reward > 0:
        # Give reward
        userdata = Extend_user.objects.get(telid=telid)
        userdata.xcoin += total_reward
        userdata.save()

        # Send msg to this user saying 'u gained xxx for inviting XX friends' !!
        bot.send_message(chat_id=query.message.chat_id,
                         text=str(total_new_friends) + " of your friends have recently top-up! You are rewarded "
                              + str(total_reward) + " x-coin.")
    else:
        bot.send_message(chat_id=query.message.chat_id,
                         text="No new friend has top-up yet. Invite more friends for more chance to win free x-coin.")
