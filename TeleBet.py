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
    Search through SQL up_id for all unclaimed reward, send one lumpsum to the user, and reset the indicators

    User must topup at least 100 x-coin, in order for upid user to gain reward 5 xcoin
    """
    query = update.callback_query

    # Check all pending reward belong to this user
    userid = get_userid_from_telid(telid)
    user_downline_data = up_id.objects.filter(upid=userid)

    # Loop each of this user's downline, and save
    total_reward = 0
    total_new_friends = 0
    for down_user in user_downline_data:
        if down_user.upid_get_reward == True:
            # Record reward
            total_reward += 300
            total_new_friends += 1

            # Reset indicator
            down_user.upid_get_reward = False
            down_user.save()

    # Give reward to user
    if total_reward > 0:
        # Give reward
        userdata = Extend_user.objects.get(telid=telid)
        userdata.xcoin += total_reward
        userdata.save()

        # Send msg to this user saying 'u gained xxx for inviting XX friends' !!
        bot.send_message(chat_id=query.message.chat_id,
                         text=str(total_new_friends) + " of your friends have joined! You are rewarded "
                              + str(total_reward) + " x-coin.")
    else:
        bot.send_message(chat_id=query.message.chat_id,
                         text="No new friend has joined yet. Invite more friends to gained free x-coin.")
