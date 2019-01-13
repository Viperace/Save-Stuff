library(Quandl)
library(quantmod)


x = Quandl("SHFE/HCK2019", api_key="YmkWCAzBmsqPfxvZJutG")
class(x)


# Find peak
pp = findPeaks(x$Close,thresh = 50)
plot(x$Close)
lines((1:nrow(x))[pp], x$Close[pp], type='b', col=4)


## Find algorithm to determine peak

findNextPeak <- function(startIndex, x, scanPeriod){
  startIndex + which.max(x[startIndex + 0:(scanPeriod - 1)]) - 1
}

findNextBottom <- function(startIndex, x, scanPeriod){
  startIndex + which.min(x[startIndex + 0:(scanPeriod - 1)]) - 1
}

findAllPeaksBottoms <- function(x, scanPeriod, restPeriod = 2, fig=TRUE)
{
  # Find first one is peak or bottom?
  indmax1 = which.max(x[1:scanPeriod]) 
  indmin1 = which.min(x[1:scanPeriod]) 
  
  if(indmax1 > indmin1){
    nextIsPeak = FALSE
  }else{
    nextIsPeak = TRUE
  }

  # Init  
  i = 1
  imax_vec = c()
  imin_vec = c()    
  while( i < length(x))
  {
    if(nextIsPeak){
      indmax = findNextPeak(i, x, scanPeriod)
      i = indmax + restPeriod
      imax_vec = c(imax_vec, indmax)
    }else{
      indmin = findNextBottom(i, x, scanPeriod)
      i = indmin + restPeriod
      imin_vec = c(imin_vec, indmin)
    }
    
    nextIsPeak = !nextIsPeak

    if(length(i) == 0){
      break
    }
  }
  
  # Plot
  if(fig){
    plot(x)
    lines(imax_vec, x[imax_vec], type='p', col=4, lwd=2)
    lines(imin_vec, x[imin_vec], type='p', col=2, lwd=2)
  }
  
  # Output
  Out = list("Peaks"=imax_vec, "Bottoms"=imin_vec)
  return(Out)
}

findAllPeaksBottoms(x, 15, 2)

