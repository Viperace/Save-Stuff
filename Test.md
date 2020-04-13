https://datascienceplus.com/modelling-dependence-with-copulas/

https://www.r-bloggers.com/how-to-fit-a-copula-model-in-r-heavily-revised-part-2-fitting-the-copula/

https://stats.stackexchange.com/questions/90283/how-to-find-conditional-probability-pxxy-y-using-copulas


require(rugarch)

data <- rnorm(1000)

plot(data)
  
spec <- ugarchspec(variance.model = list(model = "sGARCH", 
                                         garchOrder = c(1, 1), 
                                         submodel = NULL, 
                                         external.regressors = NULL, 
                                         variance.targeting = FALSE), 
                   
                   mean.model = list(armaOrder = c(1, 1), 
                                         external.regressors = NULL, 
                                         distribution.model = "norm", 
                                         start.pars = list(), 
                                         fixed.pars = list()))

garch <- ugarchfit(spec = spec, data = data, solver.control = list(trace=0))
garch@fit$coef
garch@fit$sigma
garch@fit$z

