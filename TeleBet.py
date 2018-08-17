from netunit import myGet
import json


def is_payment_sent(telid):
	""" Check if user completed payment """
	try:
		domain = myGet()	
		url = domain + "/pay/scanajax/?telid=" + telid
		jsonurl = urllib.urlopen(url)
		pay_status_json = json.loads(jsonurl.read())
		status = pay_status_json['btcovertime']
		if status == 'over':
			return True
		elif status == 'run':
			return False
		else:
			print 'Unknown payment status ' + status
			return False		
	except:
		print 'Unknown error when checking is_payment_sent '
		return False
	
def get_payment_address(telid):
	"""Function to request wallet address and get time left"""	
	url = 'http://155.254.49.141:8111/pay/buybtc/?data=buy&telid=' + telid
	jsonurl = urllib.urlopen(url)
	j = json.loads(jsonurl.read())
	btc_address = j['getbtcaddress']
	time_left_in_sec = j['btcovertime']
	#usd_per_btc = j['usd'] ??
	#cny = j['cny'] ??
	
	return btc_address, time_left_in_sec
	

def topup_process(bot, update, offset_sec=60):
	'''Initiate topup process for the user. Will Print the btc address to the user'''
	telid = update.message.chat_id
	
	general_msg = "Notice: x-coin is automatically credited to your balance once we receive 6 confirmation from your Bitcoin. \
		You can send any amount of Bitcoin, they are exchanged at this rate \
		\n	0.0001 BTC = 100 x-coin "

	# Key to save to redisb
	user_btcaddress_key = telid + "__btcaddress" 
	
	# Check if got unexpired pending payment		
	if is_payment_sent(telid):
		# Get fresh address for user to send 
		new_address, time_left = get_payment_address(telid)
		time_left_sec = int(time_left)
		
		# Save the address to redisb memory. Future pulling
		expire_time = time_left_sec - offset_sec	 # Second before expired.
		redisdb.setex(user_btcaddress_key, new_address, expire_time)
		
		# Reply user
		update.message.reply_text(general_msg)
		update.message.reply_text('Please send bitcoin to this address \n' + new_address)
		update.message.reply_text('Address will expire in ' + time_left + ' sec')		
	else:
		# Load the  btc address and time left
		user_btcaddress = redisdb.get(user_btcaddress_key)			
		time_left = redisdb.ttl(user_btcaddress_key)
		
		if time_left > 0:
			# Still got time, reply user the same address 
			update.message.reply_text(general_msg)
			update.message.reply_text('Pending your bitcoin payment to this address \n' + user_btcaddress)
			update.message.reply_text('Address will expire in ' + time_left + ' sec')
		else:
			# Lock period, wait for 'get_payment_address' to gen 'over' status
			update.message.reply_text("Address expired. \nPlease do NOT send to the address and request for new \
			address after one minute")
		
		
from btchtm.models import pay_payhistory
def show_payment_history(bot, update):
	"""Function to pull sql database for user's history """
	# pay_payhistory.objects.filter(userid=update.message.chat_id)
	
	# Retrieve all history 
	
	# Filter for the last 10
	history_to_show
	
	# update.message.reply_text
	update.message.reply_text(history_to_show)
	
