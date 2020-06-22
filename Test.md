Multi-variate Copula trading
https://www.econstor.eu/bitstream/10419/147450/1/870932616.pdf

SP100 pair
https://www.econstor.eu/bitstream/10419/125514/1/844416606.pdf
  (pyramiding)
  Open based on Copula. Close based on TP and SL, or Time!
  
Zhi (2017)
https://efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2017-Athens/papers/EFMA2017_0385_fullpaper.pdf

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
	Ticker	IB		Tx		Diff 	Qty		Slippage	YTD
	--------------------------------------------------------
	MSFT	233.15	233.00	0.15	50		-$10.05
	V		188.29	189.11	-0.33	33		-$3.6
	...
	MA		53.1	53.0	0.1		121		+$5.0

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
	   "300 S", "1 min", "MIDPOINT", 1, 1, False, [])

	def historicalDataUpdate(self, reqId: int, bar: BarData):
		print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)
		
	if reqId == 4103:
		print("HistoricalDataEnd. ReqId:", reqId, "BarData", bar)
		# Save to DataManager
		ticker = request_dictionary[reqId]
		data_manager.save(ticker, bar)
