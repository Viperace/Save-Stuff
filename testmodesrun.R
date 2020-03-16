library(quantmod)
library(BatchGetSymbols)
library(timeSeries)
install.packages('BatchGetSymbols')

tickers <- c('MCHI','SPY','EWL','EWY','EWU','EWI','EWG','ES3')

BatchGetSymbols(tickers)
