# Save-Stuff

# This tells how to merge multiple images into one
https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python

Resize on-the-fly and merge


# Get Yahoo Finance data
https://stackoverflow.com/questions/49705047/downloading-mutliple-stocks-at-once-from-yahoo-finance-python


# Phone code to country
https://pypi.org/project/phone-iso3166/

# Fix announce result to use async when send_message
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Performance-Optimizations
In main(), add workers
   updater = Updater(token="xxx", workers=64) 

bring 'send_message' to a different function and add @run_async

for telid in set(all_telid):
    try:
        bot.send_message(chat_id=telid, text=msg)
        bot.send_message(chat_id=telid, text=msg2)
    except Exception, e:
        print "Cant send message to this telid " + telid

Change above loop to something like
for telid in set(all_telid):
  sendmessage_async(bot, job, telid, msg, msg2)

@run_async
def sendmessage_async(bot, job, telid, msg1, msg2):
  bot.send_message(chat_id=telid, text=msg1)
  bot.send_message(chat_id=telid, text=msg2)
  
