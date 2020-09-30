
CRO
Stephane, new sg, march, trader
head of risk - CS

2 team
	1. Data sc
	2. cybersecurity
	3. Two person left...

what has job scope chg


* Standalone 
showcase, 

* Test

* MFE, phd

Mature candidate, can help

How do he help u better...


# Wages
	Salary1 - CPF	Salary1	Salary2	Base Ann	Bonus	 Tax 	
							
2015	7703	 9,629 			 40,000 		
2016	9186	 10,186 			 44,000 		
2017	9453	 10,453 			 48,186 	 175,243 	
2018	9653	 10,653 			 39,160 	 180,098 	
2019		 13,000 				 190,749 	
2020		 13,000 					
							
							
		Average Monthly /12m basis	 Bonus 	Remark	Annual Total		
	2015	 9,600 		DBS Annual Bonus	 115,200 		
	2016	 10,100 	 44,000 	DBS Annual Bonus	 165,200 		
	2017	 10,400 	 45,000 	DBS Annual Bonus	 169,800 		
	2018	 10,876 	 43,000 	DBS Annual Bonus	 173,512 		
	2019	 13,000 	 30,000 	Cargill Sign-on Bonus	 186,000 		
	2020	 13,000 	 67,000 	Cargill AnnualBonus	 223,000 		
	2020*	 14,500 					



Shannon Entropy
Entropy will always goes larger. 
At time T, compute two possible Entropy for T+1 by assuming price Up and price down (or 4 casees for two time-steps case, UpUp, DnDn, UpDn, DnUp).
If Entropy (for price up) is larger, then long it.
(The code in the site is showing opposite direction however)
https://robotwealth.com/shannon-entropy/


Multi-variate Copula trading
https://www.econstor.eu/bitstream/10419/147450/1/870932616.pdf

SP100 pair
https://www.econstor.eu/bitstream/10419/125514/1/844416606.pdf
  (pyramiding)
  Open based on Copula. Close based on TP and SL, or Time!
  
Zhi (2017)
https://efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2017-Athens/papers/EFMA2017_0385_fullpaper.pdf

# Beautiful soup
https://stackoverflow.com/questions/33538600/how-to-automatically-download-the-files-that-have-a-download-button-on-a-webpage

https://towardsdatascience.com/https-towardsdatascience-com-how-to-download-files-in-a-lightning-speed-a8e8dcc694f7


# Target Slippage Report looks like this
	--------------------------------------------------------
	Pair Slippage		YTD
	--------------------------------------------------------
	Pair 1	-$10.05		
	Pair 2	-$3.6
	...
	Pair 5	+$5.0
	========================================================	
	TOTAL	-$5
	--------------------------------------------------------
	

	Ticker Breakdown
	--------------------------------------------------------
	Ticker	IB	Tx	Diff 	Qty		Slippage	YTD
	--------------------------------------------------------
	MSFT	233.15	233.00	0.15	50		-$10.05
	V	188.29	189.11	-0.33	33		-$3.6
	...
	MA	53.1	53.0	0.1	121		+$5.0

# Algorithm
- Pull IBKR price,	ibkr_Px (or Google Finance)
  []
- Pull executed prices , tx_Px (and qty, Na, Nb)
  [Reporter] should have this
- Compare price, per pair 
	#slippageB = sum(tx_Px - close_Px)
	slippageA = (tx_Px - ibkr_Px)*Na - (tx_Px - ibkr_Px)*Nb

# Example
	# End Time. Put 3:59pm	
	queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")

	# Put in Class
	self.reqHistoricalData(4103, ContractSamples.EuropeanStock(), queryTime,   
	   "300 S", "1 min", "MIDPOINT", 1, 1, False, [])  # <- one time basis

	def historicalDataUpdate(self, reqId: int, bar: BarData):
		if reqId == 4103:
			print("historicalDataUpdate. ReqId:", reqId, "BarData", bar)
			# Save to DataManager
			ticker = request_dictionary[reqId]
			data_manager.save(ticker, bar)


# Further Idea
- Get also VWAP for 3:59:01 to 3:59:59, available for TRADES request
- VWAP consider the whole 1min volume. But, MID is only a snapshot.
- Backtesting is based on close of the entire minute, and also works for 1 minute earlier at 3:58.

What is slippage?
- Signal generated VS actual traded 
- Traded VS data provided price.

