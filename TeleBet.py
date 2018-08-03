# In main loop
def main():
	# Message Looper VH!
	updater.job.queue.run_once(announcement_listener, 150 - 10) # start 10s earlier

# ************* VH ************
# Use gevent to run? or schedulr ?
gevent.spawn(announcement, 3, update)


# Will this block up all shit?
def announcement_listener(update, interval):
	announcement(update)
	updater.job.queue.run_once(announcement_listener, interval)  # Call the next one
		
# How to pass update?		
def announcement(update):
	refresh_interval = 1
	while True:
		first_check_game_ended = redisdb.ttl('gamesEnd')
		try:
			time.sleep(refresh_interval) 
			second_check_game_ended = redisdb.ttl('gamesEnd')
			if first_check_game_ended != second_check_game_ended:
				# DO ANNOUNCEMENT HERE
				msg = "REsult is ..."
				update.message.reply_text(msg)

		except Exception,e:
			print e
		

# Reward allocator, faster version:
for i in range(0, len(self.winners_df)):
	winner_id = self.winners_df.iloc[i]['user_id']
	winner_newcoin = self.winners_df.iloc[i]['coin_to_add']
	Extend_user.objects.filter(ext_user_id=winner_id).update(xcoin=winner_newcoin)
