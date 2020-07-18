# Alternative Data List
- TipRanks (Blogger sentiment)
- TRESS, (TipRanks and ExtractAlpha)
- alpha-DNA  (web sentiment)
- Sandalwood Advisors (Tmall transactional data)
- CFPB (US Consumer Financial Protection Bureau) consumer complaint



# Machine Learning
- Review paper: 
Shah et al, "Stock Market Analysis: A Review and Taxonomy of Prediction Techniques"
https://www.mdpi.com/2227-7072/7/2/26/pdf


# Intraday pattern


# Good Volatility, Bad Volatility, and the Cross Section of Stock Returns
Bollersev et al(2018)
- Good/Bad voliatlity can predict movement

Review:
- My backtest is showing INVERSE result of the paper. Skewness score is PROPORTIONATE to next week return
- Weekly reversal is also proportionate to next week return


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


CONCLUSION:
- As paper show, this is too good to be true
- Even without the Volatility Regime, the base strategy is crazily profitable. Problem is BID/ASK, and commission not taken into account
- Tried on V/MA, PEP/K, works on 5m interval like a charm
- By extending to 30m, with overnight holding, this strategy fails
- Adding 5bps Bid/ask and 0.005 commission, its not profitable
- No point trying the Vol Regime Shifting, knowing the base strategy fails



# Cross Asset Rotation
https://www.man.com/maninstitute/dissecting-investment-strategies-in-the-cross-section-and-time-series

# Pair Switching
https://www.quantconnect.com/tutorials/strategy-library/paired-switching

# Sentiment and Style Rotation Effect in Stocks
https://www.quantconnect.com/tutorials/strategy-library/sentiment-and-style-rotation-effect-in-stocks


