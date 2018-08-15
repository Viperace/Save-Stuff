# Save-Stuff

# This tells how to merge multiple images into one
https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python

Resize on-the-fly and merge


# Get Yahoo Finance data
https://stackoverflow.com/questions/49705047/downloading-mutliple-stocks-at-once-from-yahoo-finance-python


# Codes for read translator
update.message.chat_id 	# user_telid 
import database_record

1) add model for 'database_record', set chinese as default
  migrate it


# At every function that repy_text, first get teh user's setting 
def get_user_language(telid):
	"""Function to get user's language from redis pool. If not found, get from  SQL .
	If still not found, return default language (CHINESE)
	Return enum of language 
	Example:
		lang = get_user_language(update.message.chat_id)
		translater.look_up("Message to tell user", lang)
	"""
	user_lang_key = telid + "__settings__language"
	if redisdb.exists(user_lang_key):
		# Get from redis pool
		user_language_settings = redisdb.get(user_lang_key)
		if user_language_settings == "ENGLISH":
			return enum.ENGLISH
		elif user_language_settings == "SIMPLIFIED_CHINESE":
			return enum.SIMPLIFIED_CHINESE
		else:
			raise ValueError('Unknown language key record in redisb ' + user_lang_key)
	else:
		# Get from SQL 
		try:
			database_record = user_settings.objects.get(telid=update.message.chat_id)
			if database_record == "EN":  # TODO: Use enum
				redisdb.set("ENGLISH")
				return enum.ENGLISH
			elif database_record == "SIMPLIFIED_CH"
				redisdb.set("SIMPLIFIED_CHINESE")
				return enum.SIMPLIFIED_CHINESE
			else:
				raise ValueError('Cannot find language setting record in SQL ' + user_lang_key)
		except:
			# Still can't find, return default
			return enum.SIMPLIFIED_CHINESE


def set_user_language(telid, enumlang):
	user_lang_key = telid + "__settings__language"
	if user_language_settings == enum.ENGLISH:
		redisdb.set(user_lang_key, "ENGLISH")
	elif user_language_settings == enum.SIMPLIFIED_CHINESE:
		redisdb.set(user_lang_key, "SIMPLIFIED_CHINESE")
	else:
		print telid + " can't set " + enumlang " . No such enum?"
			
