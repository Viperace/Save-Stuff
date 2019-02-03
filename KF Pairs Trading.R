


#### Kalman Filter study to extract rolling coef #######
# See slides 40
# http://www.ece.ust.hk/~palomar/MAFS6010R_lectures/week%2012/slides_pairs_trading.pdf
rm(list=ls())

library(FKF)
library(DEoptim)
library(quantmod)
library(timeSeries)

#******* Create time-series *******
getSymbols(c('EWH', 'EWZ'))
x1 = timeSeries(EWH[,4])
x2 = timeSeries(EWZ[,4])

tmp = cbind(x1, x2)
tmp = window(tmp, start='2014-01-01', end='2016-01-01')
x1 = tmp[,1]
x2 = tmp[,2]
plot(cbind(x1, x2))

#******* Kalman Filter *******

# Array for time-varying param
# dt either a m × n (time-varying) or a m × 1 (constant) matrix.
# Tt either a m × m × n or a m × m × 1 array.
# HHt either a m × m × n or a m × m × 1 array.
# ct either a d × n or a d × 1 matrix.
# Zt either a d × m × n or a d × m × 1 array.
# GGt either a d × d × n or a d × d × 1 array.
# yt a d × n matrix.



createFKF <- function(x1, x2, var1, var2, vare){
  stopifnot(identical(dim(x1), dim(x2)))
  
  n = nrow(x1) # Num of obs
  m = 2   # Num of hidden factor
  d = 1   # Num of dimension
  
  
  dt = matrix(0, m, n)
  Tt = array(diag(2), dim=c(m, m, n))
  HHt = array(rbind(c(var1, 0),
                    c(0, var2)), dim=c(m, m, n))  
  GGt = array(vare, dim=c(d, d, n))
  ct =  matrix(0, 1, n)
  Zt = array(t(cbind(1, as.matrix(x2))), dim=c(d, m, n))
  a0 = c(0.1, 0.1)
  P0 = diag(2)
  
  yt = as.matrix(x1)
  
  Out = fkf(a0, P0, dt, ct, Tt, Zt, HHt, GGt, t(yt))
  Out
}

# Assume constant 0.1 volatility for all factor
fit = createFKF(x1, x2, 0.1, 1, .5 )

mu = timeSeries(fit$att[1,], time(x1))
gamma = timeSeries(fit$att[2,], time(x1))

eps = x1 - (mu + gamma*x2)

# ****** Show Result ********
par(mfrow=c(2,2))
plot(mu, main='mu.Kalman')
plot(gamma, main='gamma.Kalman')

plot(x1, col=2, main='x1 VS Kalman')
lines(mu + gamma*x2, col='grey')

plot(eps, main='Kalman residual')



# ***** Cointegration Test *********
fit = lm(x1 ~ 1 + x2)
summary(fit)
fit$coefficients

spread = x1 - fit$coefficients[2]*x2
colnames(spread) = paste0(colnames(x1), '-', colnames(x2))
dspread = spread - lag(spread, 1)
par(mfrow=c(2,2))
plot(spread, main='Sprd');

qqnorm(dspread); qqline(removeNA(dspread))
adf.test(fit$residuals)
pp.test(fit$residuals)



#**** Mean Reversion ****
plot(x1/as.numeric(x1[1]), ylim = c(0.5, 1.5))
lines(x2/as.numeric(x2[1]), col=2)


#**** No use *******
myObj <- function(par){
  fit = createFKF(x1, x2, par[1], par[2], par[3] )
  -fit$logLik
}

optim(c(1,1,1), myObj, lower = c(0.0001, 0.0001, 0.0001), upper=c(10, 10, 10), method='L-BFGS-B')
# fit = DEoptim(myObj, lower = c(0.0001, 0.0001, 0.0001), upper=c(10, 10, 10))


#***** Number of Crossing ******
getPointsOfCrossing <- function(x1, x2){
  stopifnot(nrow(x1) == nrow(x2))
  
  # Rescale
  xresc = cbind(x1/x1[1], x2/x2[1])
  
  # Find number of cross
  gt = xresc[, 1] > xresc[, 2]
  indexOfCross = which(gt != lag(gt, 1))
  
  indexOfCross
}


cross.vec = c()
for(y in c(2014, 2015)){
  sd = paste0(y, '-01-01')
  ed = paste0(y, '-12-31')
  
  a = window(x1, start=sd, end=ed)
  b = window(x2, start=sd, end=ed)
  
  cross.vec = c(cross.vec,  length(getPointsOfCrossing(a, b)))
}





tmp = cbind(x1/as.numeric(x1[1]), x2/as.numeric(x2[1]))
plot(tmp[,1])
lines(tmp[,2], type='l', col=2)


# Number of Crossing
# write.csv(tmp, 'd:/test.csv')

computeDist <- function(x, y, lateStart=0){
  Out = cbind(x, y)
  Out = timeSeries(Out)
  
  # Remove
  if(lateStart > 0){
    Out = Out[-c(1:lateStart),]
  }
  
  # Normalize
  Out2 = cbind(Out[,1]/as.numeric(Out[1,1]),
               Out[,2]/as.numeric(Out[1,2]))
  
  
  
  plot(Out2[,1], ylim = c(min(Out2), max(Out2)))
  lines(Out2[,2], col=2)
  
  # Output
  N = nrow(Out2)
  sqrt(sum((Out2[,1] - Out2[,2])^2))/N
}

lag.vec = seq(0, 3000, 30)
dist.vec = c()
for(i in lag.vec){
  dist.vec = c(dist.vec, computeDist(SSO[,6], MDY[,6], i))
}
names(dist.vec) = lag.vec

par(mfrow=c(2,1))
plot(lag.vec, dist.vec, type='b')
computeDist(SSO[,6], MDY[,6], 0)

x1 = log(timeSeries(SSO[,4]))
x2 = log(timeSeries(MDY[,4]))

