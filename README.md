# Save-Stuff

# This tells how to merge multiple images into one
https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python

Resize on-the-fly and merge


# Get Yahoo Finance data
https://stackoverflow.com/questions/49705047/downloading-mutliple-stocks-at-once-from-yahoo-finance-python


# Phone code to country
https://pypi.org/project/phone-iso3166/

# Today Error  File "btcbot.py", line 447, in start
.7/site-packages/django/db/backends/utils.py", line 79, in execute
    return super(CursorDebugWrapper, self).execute(sql, params)
  File "/usr/local/lib/python2.7/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
  File "/usr/local/lib/python2.7/site-packages/django/db/utils.py", line 97, in __exit__
    six.reraise(dj_exc_type, dj_exc_value, traceback)
  File "/usr/local/lib/python2.7/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
  File "/usr/local/lib/python2.7/site-packages/django/db/backends/mysql/base.py", line 124, in execute
    return self.cursor.execute(query, args)
  File "/usr/local/lib/python2.7/site-packages/MySQLdb/cursors.py", line 205, in execute
    self.errorhandler(self, exc, value)
  File "/usr/local/lib/python2.7/site-packages/MySQLdb/connections.py", line 36, in defaulterrorhandler
    raise errorclass, errorvalue
OperationalError: (2006, 'MySQL server has gone away')
2018-08-24 09:58:09,441 - telegram.ext.dispatcher - ERROR - An uncaught error was raised while processing the update
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/site-packages/telegram/ext/dispatcher.py", line 279, in process_update
    handler.handle_update(update, self)
  File "/usr/local/lib/python2.7/site-packages/telegram/ext/commandhandler.py", line 173, in handle_update
    return self.callback(dispatcher.bot, update, **optional_args)
  File "btcbot.py", line 447, in start
    user_settings.objects.get_or_create(telid=telid, language='ENGLISH')
  File "/usr/local/lib/python2.7/site-packages/django/db/models/manager.py", line 127, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/usr/local/lib/python2.7/site-packages/django/db/models/query.py", line 405, in get_or_create
    return self.get(**lookup), False
  File "/usr/local/lib/python2.7/site-packages/django/db/models/query.py", line 328, in get
    num = len(clone)
  File "/usr/local/lib/python2.7/site-packages/django/db/models/query.py", line 144, in __len__
    self._fetch_all()
  File "/usr/local/lib/python2.7/site-packages/django/db/models/query.py", line 965, in _fetch_all
    self._result_cache = list(self.iterator())
  File "/usr/local/lib/python2.7/site-packages/django/db/models/query.py", line 238, in iterator
    results = compiler.execute_sql()
  File "/usr/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py", line 840, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python2.7/site-packages/django/db/backends/utils.py", line 79, in execute
    return super(CursorDebugWrapper, self).execute(sql, params)
  File "/usr/local/lib/python2.7/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
  File "/usr/local/lib/python2.7/site-packages/django/db/utils.py", line 97, in __exit__
    six.reraise(dj_exc_type, dj_exc_value, traceback)
  File "/usr/local/lib/python2.7/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
  File "/usr/local/lib/python2.7/site-packages/django/db/backends/mysql/base.py", line 124, in execute
    return self.cursor.execute(query, args)
  File "/usr/local/lib/python2.7/site-packages/MySQLdb/cursors.py", line 205, in execute
    self.errorhandler(self, exc, value)
  File "/usr/local/lib/python2.7/site-packages/MySQLdb/connections.py", line 36, in defaulterrorhandler
    raise errorclass, errorvalue
OperationalError: (2006, 'MySQL server has gone away')
