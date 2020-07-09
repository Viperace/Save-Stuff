
# Intraday pattern


# Good Volatility, Bad Volatility, and the Cross Section of Stock Returns
Bollersev et al(2018)
- Good/Bad voliatlity can predict movement

# Intraday Patterns in the Cross-section of Stock Return
Heston et al
- Cross section time is cyclical

# An Improved Pairs Trading Strategy Based on Switching Regime Volatility
https://alphaedge.io/trading-strategies/momentum-investing/Tactical-Pair-Switching/
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2636212

Pair 
- Pre-defined (SPY, QQQ)

Calibration
- Period:	
	- 4500 data (-> 3months, assuming 10mins freq )
- MixGaussian to determine Regime 
- Beta: min variance ratio
	Spread = p1 - Beta*p2
	Beta = rho * sig_1/Sig_2

Signal:
- High or Low Regime
	- high-volatility regimes correspond to periods with rolling standard deviation above
	the dashed line
	- Treshold = from trainig sets average
- Bollinger Band Hi
- Bollinger Band Low
	-> Use Sigma from MixGaussian model.



# Cross Asset Rotation
https://www.man.com/maninstitute/dissecting-investment-strategies-in-the-cross-section-and-time-series

# Pair Switching
https://www.quantconnect.com/tutorials/strategy-library/paired-switching

# Sentiment and Style Rotation Effect in Stocks
https://www.quantconnect.com/tutorials/strategy-library/sentiment-and-style-rotation-effect-in-stocks

