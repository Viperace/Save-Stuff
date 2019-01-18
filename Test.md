rm(list=ls())
setwd('C:/Users/voonhooiliew/Desktop/CS Model/')

library(data.table)
library(lubridate)
library(timeSeries)
library(FKF)

#--Create Futures Panel from raw data
rawData = fread('COMSPOT_BM_AL_LME_Fu (2).csv')
#head(rawData)
#tmp[1:5,1:5]

rawDataHead = colnames(rawData)[-1]
rawMaturity = dmy(substr(rawDataHead,1,11))

# Create raw panel
X = data.frame(rawData[,-1])
rownames(X) = rawData$Date
colnames(X) = rawMaturity

#****** Create maturity and price list  ******
Xmat = c()
Xprice = c()
for(i in 1:nrow(X)){
  t0 = ymd(rownames(X)[i])
  tmp = removeNA(t(X[i,]))
  
  # Maturity
  matVec = t(difftime(ymd(rownames(tmp)), t0, units = 'days'))
  Xmat[[i]] = matVec

  # PRices
  Xprice[[i]] = t(matrix(tmp))
  print(i)
}
names(Xmat) = rownames(X)
names(Xprice) = rownames(X)


#****** Create equal maturity price data  ******
std_tenor = c(
  seq(1/365, 3/12, 1/365),   # 1m-3m
  seq(3/12 + 1/52, 52, 1)/52,  # 3m-1y
  seq(1 + 1/12, 5, 1/12)) #1y-5y
Xstd = matrix(NA, nrow(X), length(std_tenor))
rownames(Xstd) = rownames(X)
for(i in 1:nrow(X)){
  t0 = ymd(rownames(X)[i])
  tvec = Xmat[[i]]/365
  
  if(length(Xprice[[i]]) < 10){
    warning(paste("Insufficient datapoint in ", i))
  }else{
    tmp = approx(tvec, Xprice[[i]], xout = std_tenor)
    Xstd[i,] = tmp$y
  }
}
Xstd = timeSeries(Xstd)

logX = log(Xstd)


# ********* Calibration using KF *********** 
#   zt = Ht * xt + dt + vt,   R
#   xt = At * x(t-1) + ct + et,   Q
#
# Three-Factors
# 16 Parameter:
#   k2, k3
#   sig1, sig2, sig3
#   lam1, lam2, lam3
#   rho12, rho13, rho23
#   mu, zi

par=c('k2'=1, 'k3'=1,
      'sig1'=1, 'sig2'=1, 'sig3'=1, 
      'lam1'=1, 'lam2'=1, 'lam3'=1, 
      'rho12'=0.1, 'rho13'=0.1, 'rho23'=0.1, 
      'mu' = 1,
      'zi' = 1
      )

delt = 1/252
m = length(std_tenor)
myObj <- function(par){
  At = diag(c(1, 
              1-par['k2']*delt,
              1-par['k3']*delt))
  
  ct = rep(0, m)
  
  Ht = cbind(rep(1, m),
          exp(-par['k2']*std_tenor),
          exp(-par['k3']*std_tenor))
  
  Q = rbind(c(par['sig1']^2, par['sig1']*par['sig2']*par['rho12'], par['sig1']*par['sig3']*par['rho13']),
            c(par['sig1']*par['sig2']*par['rho12'], par['sig2']^2, par['sig2']*par['sig3']*par['rho23']),
            c(par['sig1']*par['sig3']*par['rho13'], par['sig2']*par['sig3']*par['rho23'], par['sig3']^2))
  Q = Q *delt
  
  R = diag(m)*par['zi']
  
  # Get last term
  sig = c(par['sig1'], par['sig2'], par['sig3'])
  kappa = c(1, par['k2'], par['k3'])
  lambda = c(par['lam1'], par['lam2'], par['lam3'])
  rho = rbind( c(1, par['rho12'], par['rho13']),
               c(par['rho12'], 1, par['rho23']),
               c(par['rho13'], par['rho23'], 1))
  sumterm = 0
  for(i in 1:3){
    for(j in 1:3){
      if(i != j){
        tkt = std_tenor[]
        sumterm = sumterm + 
          sig[i]*sig[j]*rho[i,j]*(1 - exp(-(kappa[i]+kappa[j])*tkt))/(kappa[i]+kappa[j])
      }
    }
  }
  sumterm = 0.5 * sumterm
  
  par['mu']*t +
  (par['mu'] - par['lam1'] + 0.5*par['sig1']^2)*tkt -
  (1-exp(-par['k2']*tkt))*par['lam2']/par['k2'] -
  (1-exp(-par['k3']*tkt))*par['lam3']/par['k3'] + 
  sumterm

 
  # in FkF package VS this notation
  #         FKF         CS model
  # State   alpha         x
  #         Tt             Ht
  #         dt             ct
  #         H*eta          Q
  # Obs     yt             zt
  #         ct             vt
  #         Zt             At
  #         G*eta          R
  
  a0 = c(1, 1, 1) # Inital value for state var
  P0 = c(1, 1, 1) # var
  
  -fkf(a0, P0, ct, vt, Ht, At, 
       HHt = Q, GGt = R,
       yt=t(logX))$logLik
}






