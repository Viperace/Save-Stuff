library(lubridate)

compute_expected_dr <- function(r0, fomc_dates, today, sofr_futures) 
{
  
  # convert to Date
  fomc_dates <- as.Date(fomc_dates)
  today <- as.Date(today)
  
  # months corresponding to futures
  months_vec <- seq(floor_date(today, "month"),
                    by = "1 month",
                    length.out = length(sofr_futures))
  
  # implied average monthly rates
  r_month <- 100 - sofr_futures

  # expected rate recursion
  E_r_prev <- r0
  
  expected_dr <- rep(NA, length(sofr_futures)) # Init
  for(i in seq_along(months_vec)) {
    
    m_start <- floor_date(months_vec[i], "month")
    m_end   <- ceiling_date(m_start, "month") - days(1)
    
    # check if meeting inside this month
    meeting <- fomc_dates[fomc_dates >= m_start & fomc_dates <= m_end]
    
    # NO meeting
    if(length(meeting) == 0) { 
      E_r_prev <- r_month[i]
      expected_dr[i] <- 0
      
    } else { # Got meeting
      
      meeting_day <- meeting[1]
      
      days_total <- as.numeric(m_end - m_start + 1)
      days_after <- as.numeric(m_end - meeting_day)
      
      w2 <- days_after / days_total
      
      if(w2 == 0) {
        expected_dr[i] <- 0
      } else {
        expected_dr[i] <- (r_month[i] - E_r_prev) / w2
      }
      
      E_r_prev <- r_month[i]
    }
  }
  
  #  Save output
  Out = data.frame(
    month = months_vec,
    sofr_price = sofr_futures,
    implied_rate = r_month,
    expected_dr = expected_dr
  )

  return(Out)
}


# with bid/ask
compute_expected_dr_range_TODEL <- function(r0, fomc_dates, today, sofr_bid, sofr_ask) 
{
  
  fomc_dates <- as.Date(fomc_dates)
  today <- as.Date(today)
  
  months_vec <- seq(floor_date(today, "month"),
                    by = "1 month",
                    length.out = length(sofr_bid))
  
  r_month_bid <- 100 - sofr_bid
  r_month_ask <- 100 - sofr_ask
  
  expected_dr_min <- rep(NA, length(sofr_bid))
  expected_dr_max <- rep(NA, length(sofr_bid))
  
  E_r_prev_min <- r0
  E_r_prev_max <- r0
  
  for(i in seq_along(months_vec)) {
    
    m_start <- floor_date(months_vec[i], "month")
    m_end   <- ceiling_date(m_start, "month") - days(1)
    
    meeting <- fomc_dates[fomc_dates >= m_start & fomc_dates <= m_end]
    
    if(length(meeting) == 0) {
      
      E_r_prev_min <- r_month_bid[i]
      E_r_prev_max <- r_month_ask[i]
      
      expected_dr_min[i] <- 0
      expected_dr_max[i] <- 0
      
    } else {
      
      meeting_day <- meeting[1]
      
      days_total <- as.numeric(m_end - m_start + 1)
      days_after <- as.numeric(m_end - meeting_day)
      
      w2 <- days_after / days_total
      
      if(w2 == 0) {
        
        expected_dr_min[i] <- 0
        expected_dr_max[i] <- 0
        
      } else {
        
        # worst / best cases
        expected_dr_min[i] <- (r_month_ask[i] - E_r_prev_max) / w2
        expected_dr_max[i] <- (r_month_bid[i] - E_r_prev_min) / w2
        
      }
      
      E_r_prev_min <- r_month_bid[i]
      E_r_prev_max <- r_month_ask[i]
    }
  }
  
  data.frame(
    month = months_vec,
    sofr_bid = sofr_bid,
    sofr_ask = sofr_ask,
    implied_rate_bid = r_month_bid,
    implied_rate_ask = r_month_ask,
    expected_dr_min = expected_dr_min,
    expected_dr_max = expected_dr_max
  )
}


compute_expected_dr_range <- function(r0, fomc_dates, today, sofr_bid, sofr_ask)
{
  res_bid <- compute_expected_dr(r0, fomc_dates, today, sofr_bid)
  res_ask <- compute_expected_dr(r0, fomc_dates, today, sofr_ask)
  
  data.frame(
    month = res_bid$month,
    sofr_bid = sofr_bid,
    sofr_ask = sofr_ask,
    implied_rate_bid = res_bid$implied_rate,
    implied_rate_ask = res_ask$implied_rate,
    expected_dr_min = pmin(res_bid$expected_dr, res_ask$expected_dr),
    expected_dr_max = pmax(res_bid$expected_dr, res_ask$expected_dr)
  )
}


r0 <- 3.68

today <- "2026-03-06"

fomc_dates <- c(
  "2026-03-18",
  "2026-04-29",
  "2026-06-17"
)

sofr_fut <- c(
  96.3325,
  96.335,
  96.36,
  96.3900
)

compute_expected_dr(r0, fomc_dates, today, sofr_fut)


#---- with bid/ask -------
sofr_bidask = rbind(
  c(96.335, 96.33),
  c(96.340, 96.335),
  c(96.365, 96.36),
  c(96.39, 96.385)
)
compute_expected_dr_range(r0, fomc_dates, today, sofr_bidask[,2], sofr_bidask[,1]) 
  


########## Hedge Ratio ##############
# $1 poly = 0.25bps exposure
# 
# 1 bp SOFR = $25 => $1 Poly = $6.25 SOFR risk
# $1 Poly = $6.25 SOFR risk
#
# $1 Poly = 0.25 SOFR contracts

