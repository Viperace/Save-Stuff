
#************************************************************************************************
# Function to compute PNL of trade on any OHLC time-series, with TP, SL limit level and Time-Stop defined.
# If any SL and TP not hit, exit at last given bar
#   Trade direction is imply by TP and SL level, (I.e. TP > SL, means long trade)
#
# Input:
#   @x,   OHLC time-series or xts object.
#   @entryBarNumber,   Number of bar to enter the trade (assume done at Close price)
#   @TPlevel, Take profit level. 
#   @SLlevel, SL level
#   @nBarToTimeStop=NULL,     NULL, then will pick the last bar in x
#
# Example:
# getSymbols("SPY)
# entryBarNumber = 20   # Number of bar the entry is being done (assume done at close)
#   simulateBracketTrade(tail(SPY, 200), TPlevel=400, SLlevel=200, 10, nBarToTimeStop=50)
#************************************************************************************************
simulateBracketTrade <- function(x, TPlevel, SLlevel, entryBarNumber=1, nBarToTimeStop=NULL)
{
  stopifnot(ncol(x) >= 4) # Need OHLC
  stopifnot(all(x[,2] >= x[,3]))
  stopifnot(TPlevel != SLlevel)
  
  # Determine trade direction
  side = ifelse(TPlevel > SLlevel, 1, -1)
  
  if(is.null(nBarToTimeStop)){
    indToStop = nrow(x)
  }else{
    indToStop = entryBarNumber + nBarToTimeStop
    indToStop = min(indToStop, nrow(x))
  }
  
  # Entry price
  entryPrice = as.numeric(x[entryBarNumber, 4])

  # Determine if TP or SL hit first
  hi = x[, 2]
  low = x[, 3]
  
  if(side == 1){ #Long side
    inds = which(hi >= TPlevel)
    indHitTP = inds[inds > entryBarNumber][1]
    
    inds = which(SLlevel >= low )
    indHitSL = inds[inds > entryBarNumber][1]
    
  }else{ # Short side
    inds = which(hi >= SLlevel)
    indHitSL = inds[inds > entryBarNumber][1]
    
    inds = which(TPlevel >= low )
    indHitTP = inds[inds > entryBarNumber][1]
  }
  
  #--Compare all SL, TP , and Time-Stop
  outcomes = c('SL'=indHitSL, 'TP'=indHitTP, 'Time'=indToStop)
  tmp = outcomes[which.min(c(indHitSL, indHitTP, indToStop))]
  outcome = names(tmp)
  
  if(outcome == 'SL'){
    indExit = indHitSL
    exitLevel = SLlevel
  }else if(outcome == 'TP'){
    indExit = indHitTP
    exitLevel = TPlevel
  }else if(outcome == 'Time'){
    indExit = indToStop
    exitLevel = as.numeric(x[indToStop, 4])
  }else{
    stop('Cannot be... No outcome')
  }

  #abline(v=time(x[entryBarNumber]), col=4)
  #abline(h=TPlevel, col='green', lty=2)
  #abline(h=SLlevel, col='red', lty=2)
  
  #--Output
  exitTime = time(x[indExit,])
  duration = indExit - entryBarNumber
  PNL = side*(exitLevel - entryPrice)
  
  Out = c()
  Out$outcome = outcome
  Out$entryTime = time(x[entryBarNumber,])
  Out$exitTime = exitTime
  Out$duration = duration
  Out$PNL = PNL
  Out
}

