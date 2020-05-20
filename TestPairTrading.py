
######### Init R Copula function  #########
import rpy2.robjects as robjects
import rpy2.interactive as R
import rpy2.interactive.packages # this can take few seconds

R.packages.importr("VineCopula")
par1 = 0.05
par2 = 0
family = 3

robjects.r('''
		copulaH <- function(u, v, par1, par2, family) {
			myCop = VineCopula::BiCop(family = family, par = par1, par2, par2) 
			BiCopHfunc2(0.01, 0.03, myCop)
		}
		
		getSignal <- function(copulaH, thres){
			if(copulaH > thres){
				return(1)
			}else if(copulaH < -thres){
				return(-1)
			}else{
				...
			}
		}
		''')
		
copulaH = robjects.r['copulaH']
getSignal = robjects.r['getSignal']


######### Init Param #########
engineStopTime = tomorrow + 4hour 
signalingTime = "03:40am"
executionTime = "03:44am"
LAST_SIGNAL = None


######### Main Prog #######
while True 
	time.sleep(1)

	if Time.Time < engineStopTime:
		if Time.Time > executionTime: 

			##### Send signal for position #####
			if LAST_SIGNAL == 1:
				#? 
			else if LAST_SIGNAL == -1:
				#? 
			else if LAST_SIGNAL == 0:
				#? 
			else
				print("??ERROR SIGNAL?")
				
		else if Time.Time > signalingTime:
			##### Get Price and process to signal #####
			px1 = SpreadListener.Price1
			px2 = SpreadListener.Price2
			
			# Convert to ECDF
			u1 = ecdf(px1)
			u2 = ecdf(px2)
				
			# Run R code in its Global env
			x = copulaH(u1, u2, par1, par2, family )	
			LAST_SIGNAL = getSignal(x)

		
	else:
		print("Engine Stop.")
		break
	
# Receive at TestWrapper (Listener)
class TestWrapper(wrapper.EWrapper):
	def realtimeBar(self, reqId: TickerId, time:int, open_: float, high: float, low: float, close: float,
		volume: int, wap: float, count: int):
	
		if reqId == 3001:
			super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
			print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open_, high, low, close, volume, wap, count))
			
			SpreadListener.UpdateStock1(close, time)
			
		if reqId == 3002:
			super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
			print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open_, high, low, close, volume, wap, count))
			
			SpreadListener.UpdateStock2(close, time)
			

class SpreadListener():
	@property
	price1 = None 	
	price2 = None
	timeStamp1 = None
	timeStamp2 = None
	beta = 1.3
	
	def Spread():
		self.lastPrice1 - self.beta*self.lastPrice2
	
	def GetTimeStamp():
		[Earliest=min(timeStamp1, timeStamp2), 
		Latest=max(timeStamp1, timeStamp2), 
		Lag = timeStamp2-timeStamp1]
	
	def UpdateStock1(price, timeStamp):
		self.price1 = price
		self.timeStamp1 = timeStamp
	
	def UpdateStock2(price, timeStamp):
		self.price2 = price
		self.timeStamp2 = timeStamp

	
