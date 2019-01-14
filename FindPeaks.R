library(Quandl)
library(quantmod)
library(timeSeries)


tmp = Quandl("SHFE/HCK2019", api_key="YmkWCAzBmsqPfxvZJutG")
set.seed(123)
x = cumprod(1 + rnorm(100, 0.05/252, 0.2/sqrt(252)))
plot(x)


# Find peak
pp = findPeaks(x$Close,thresh = 50)
plot(x$Close)
lines((1:nrow(x))[pp], x$Close[pp], type='b', col=4)


#************************************************************
## Algorithm to determine peak
#************************************************************

findNextPeak <- function(startIndex, x, scanPeriod){
  startIndex + which.max(x[startIndex + 0:(scanPeriod - 1)]) - 1
}

findNextBottom <- function(startIndex, x, scanPeriod){
  startIndex + which.min(x[startIndex + 0:(scanPeriod - 1)]) - 1
}

#************************************************************
# Given a vector or timeSeries, return all localized peak/bottom
# Algorithm:
#   1) from 1st point, check for next 'scanPeriod' for the max and min. 
#   2) From N1, (supposed its min) check for the max index within next 'scanPeriod', N2
#   3) From N2, (supposed its max), check for the min index within next 'scanPeriod', N3
#   4) ... Keep looping till all alternate Max/Min point is found
#
# Input:
#   @x,           vector or time-series to analyze
#   @scanPeriod,  scan period to check for local min/max
#   @restPeriod,  minimum spacing of nearby Peak and Bottom. Minimum=1
#       (e.g. if restPeriod = 1, point i is bottom, then point i+1 can be peak)
#
# Example:
#     x = cumprod(1 + rnorm(100, 0.05/252, 0.2/sqrt(252))) #Generate time-series 
#     aa = findAllPeaksBottoms(x, 30)  # Find the peak/bottoms
#     removeInvalidPeakBottom(aa$Peaks, aa$Bottoms, x) # Filter out invalid point
#************************************************************
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

#************************************************************
# Function to remove peak/bottoms that are spaced too closely.
# 
# -If current peak point is X, next bottom must be lower than X by Thres amount
# -If current bottom point is X, next peak must be higher than X by Thres amount
# This algortihm iterate every point i, i+1, and if (i,i+1) found to
# violate above rules, both points are deleted
#************************************************************
removeInvalidPeakBottom <- function(peaks, bottoms, x, thres=0, fig=TRUE)
{
  peakFirst = min(bottoms) > min(peaks)
    
  n = length(c(peaks, bottoms))
 
  
  # Create tuples of [peak,btm], [btm, peak]
  pairs = c()
  for(i in 1:n){
    pairs = rbind(pairs, c("Bottoms"=bottoms[i], "Peaks"=peaks[i]))
    
    if(peakFirst){
      pairs = rbind(pairs, c("Bottoms"=bottoms[i], "Peaks"=peaks[i+1]))
    }else{
      pairs = rbind(pairs, c("Bottoms"=bottoms[i+1], "Peaks"=peaks[i]))
    }
  }
  pairs = removeNA(pairs)
  
  # Loop pairs and check 
  bad_bottoms = c()
  bad_peaks = c()
  for(i in 1:nrow(pairs)){
    if( x[pairs[i,'Bottoms']] + thres < x[pairs[i,'Peaks']]){
      next # OK
    }else{
      bad_bottoms = c(bad_bottoms, pairs[i,'Bottoms'])
      bad_peaks = c(bad_peaks, pairs[i,'Peaks'])
    }
  }
  

  # Output
  cleansed_bottoms = setdiff(bottoms, bad_bottoms)
  cleansed_peaks = setdiff(peaks, bad_peaks)
  
  # Plot
  if(fig){
    plot(x)
    lines(cleansed_peaks, x[cleansed_peaks], type='p', col=4, lwd=2)
    lines(cleansed_bottoms, x[cleansed_bottoms], type='p', col=2, lwd=2)
  }
  
  Out = list("Peaks"=cleansed_peaks, "Bottoms"=cleansed_bottoms)
  Out
  
}

x = x[-c(1:15)]
a = findAllPeaksBottoms(x, 15, 2)
newa = removeInvalidPeakBottom(a$Peaks, a$Bottoms, x)
plot(x)
lines(newa$Peaks, x[newa$Peaks], type='p', col=4, lwd=2)
lines(newa$Bottoms, x[newa$Bottoms], type='p', col=2, lwd=2)

x = cumprod(1 + rnorm(100, 0.05/252, 0.2/sqrt(252))) #Generate time-series 
aa = findAllPeaksBottoms(x, 15)  # Find the peak/bottoms
aa
removeInvalidPeakBottom(aa$Peaks, aa$Bottoms, x, 0) # Filter out invalid point
