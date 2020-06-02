Multi-variate Copula trading
https://www.econstor.eu/bitstream/10419/147450/1/870932616.pdf

SP100 pair
https://www.econstor.eu/bitstream/10419/125514/1/844416606.pdf
  (pyramiding)
  Open based on Copula. Close based on TP and SL, or Time!
  
Zhi (2017)
https://efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2017-Athens/papers/EFMA2017_0385_fullpaper.pdf


tz = pytz.timezone("Singapore")
datetime.datetime.now(tz) > datetime.datetime(2020, 5, 28, 7, 9, tzinfo=tz)

# test
from dateutil.tz import gettz
tz = gettz("America/New_York")
closeTime = dt.datetime(2020, 6, 2, 16,00, tzinfo=tz)
closeTime - dt.datetime.now(tz)


# Define Trading day and Execution time
trading_day = str(dt.datetime.now(tz))[0:10]
yyyy = int(trading_day[0:4])
mm = int(trading_day[6:7])
dd = int(trading_day[9:10])
signal_time = dt.datetime(yyyy, mm, dd, 15, 43, tzinfo=tz)
execution_time = dt.datetime(yyyy, mm, dd, 15, 44, tzinfo=tz)
stop_time =  dt.datetime(yyyy, mm, dd, 16, 5, tzinfo=tz)
