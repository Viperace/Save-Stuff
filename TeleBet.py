def start():
	# User start 
	# Get telid, from args[0] get upid
	get_or_set_upid(telid, upid)
	
	
# Method 2. Call from a button.
def claim_reward():
	'''
	Process to give all unclaimed reward to user, send a message telling him that. 
	Search through SQL up_id for all unclaimed reward, send one lumpsum to the user, and reset the indicators
	'''
	# Check all pending reward belong to this user
	userid = get_userid_from_telid(user_telid)
	user_downline_data = up_id.objects.filter(upid=userid)
	
	# Loop each of them and provide reward
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
		bot.send_message(chat_id=update.message.chat_id,
                         text=str(total_new_friends) + " of your friends have joined! You are rewarded " 
						 + str(total_reward) + " x-coin.")
	else:
		bot.send_message(chat_id=update.message.chat_id,
                         text="No new friend has joined yet. Invite more friends to gained free x-coin.")


def get_or_set_upid(user_telid, upid):
	''' 
	Function to save upid of a particular userid into SQL.
	Provided if the user do not already have existing upid.
	'''
	# Get corresponding userid
	userid = get_userid_from_telid(user_telid)
	
	# Check if SQL already contain it 
	if up_id.objects.filter(userid=userid).count() == 0:
		try:
			#up_id.objects.get_or_create(userid=userid, upid=upid)
			up_id.objects.get_or_create(userid=userid, upid=upid, upid_get_reward=True)
			return True
		except:
			print "Fail to create upid for user " + str(user_telid)
			return False
	else:
		# Already contain up_id.
		print "User " + str(user_telid) + " already contain up_id "
		return False

def get_userid_from_telid(telid):
	''' Function to convert userid to telid '''
	try:
		userdata = Extend_user.objects.get(telid=telid)
		return userdata.ext_user_id
	except:
		print "Error finding telid of user " + str(telid)
		return None


def reward_screen_keyboard(chat_id, update):
    keyboard = [[InlineKeyboardButton(unquote("Invitation Code"), callback_data='xzxzxz'), ],
                [InlineKeyboardButton("Check/Redeem Reward", callback_data='claim_reward')]
				]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Invite Friends:', reply_markup=reply_markup, )


# Method X - NO USE 
def downline_user_start():
	# Check if he is first time login. If up_id in SQL does not contains it, then yes
	get_or_set_upid(telid)
	
	# Give reward to the user's upid, if not yet 
	userid = get_userid_from_telid(user_telid)
	user_upid_data = up_id.objects.get(userid=userid)
	if user_upid_data.upid_get_reward == True:
		# Up_id is eligible for reward
		up_user = Extend_user.objects.get(ext_user_id=user_upid_data.upid)
		
		# Add reward to him
		up_user.xcoin += 300
		up_user.save()
		
		# Set the indicator back
		user_upid_data.upid_get_reward = False
		user_upid_data.save()
	else:
		# Reward already given
		pass
