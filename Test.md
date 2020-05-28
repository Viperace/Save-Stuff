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

# Check this. Why all signal on simultaneously ?
library(VineCopula)
library(quantmod)

getSymbols(c("V", "MA"))

panel = as.timeSeries(cbind(V[,6], MA[,6]))
panel = window(panel, start='1111-11-11', end='2020-05-20')
ret = getReturn(panel)

efun1 = ecdf(as.numeric(tail(ret[,1], 1000)))
efun2 = ecdf(as.numeric(tail(ret[,2], 1000)))

prevPrice = c(191.2975006,	297.6832886)  #<- questionable ?
price = c(188.92,	292.575)    # prices at 5/27/2020	22:49:31

liveret = log(price/prevPrice)

UU = efun1(liveret[1])
VV = efun2(liveret[2])

BiCopHfunc(UU, VV, 2, 0.886775831483175, 2.54308833968644 )
