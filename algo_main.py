## MMF1921 (2023) - Project 2
# 
# The purpose of this program is to provide a template with which to
# develop Project 2. The project requires you to test different models 
# (and/or different model combinations) to create an asset managshortement
# algorithm. 

# This template will be used by the instructor and TA to assess your  
# trading algorithm using different datasets.

# PLEASE DO NOT MODIFY THIS TEMPLATE

import pandas as pd
import numpy as np
import datetime as dt
import time

# Program Start
###########################################################################
## 1. Read input files 
###########################################################################

# Input file names
assetData  = 'MMF1921_AssetPrices_3.csv'
factorData = 'MMF1921_FactorReturns_3.csv'

# Initial budget to invest ($100,000)
initialVal = 100000

# Length of investment period (in months)
investPeriod = 6

# Load the stock weekly prices
adjClose = pd.read_csv(assetData, index_col=0)
adjClose.index = pd.to_datetime(adjClose.index)

# Load the factors weekly returns
factorRet = pd.read_csv(factorData, index_col=0)
factorRet.index = pd.to_datetime(factorRet.index)
riskFree = factorRet['RF']
factorRet = factorRet.drop(columns='RF')

# Identify the tickers and the dates 
tickers = adjClose.columns
dates   = factorRet.index

# Calculate the stocks' weekly EXCESS returns
returns = adjClose.pct_change(1).dropna().sub(riskFree.values, axis=0)

# Align the price table to the asset and factor returns tables by
# discarding the first observation.
adjClose = adjClose.tail(-1)



testStart = pd.to_datetime(returns.index[0]) + np.timedelta64(5,'Y')

# Start of out-of-sample test period 
testStart = pd.to_datetime(returns.index[0]) + np.timedelta64(5,'Y')

# End of the first investment period
testEnd = testStart + np.timedelta64(investPeriod,'M') - np.timedelta64(1,'D')


# End of calibration period (note that the start date is the first
# observation in the dataset)
calEnd = testStart - np.timedelta64(1,'D')

# Total number of investment periods
NoPeriods = int(np.ceil((pd.to_datetime(returns.index[-1]) - testStart).days / (30.44*investPeriod) ))

# Number of assets      
n = len(adjClose.columns)

###########################################################################
## 2. Run your program
# 
# This section will run your Project1_Function in a loop. The data will be
# loaded progressively as a growing window of historical observations.
# Rebalancing will take place after every loop
###########################################################################

# Preallocate space for the portfolio weights (x0 will be used to calculate
# the turnover rate)
x = np.empty(shape=(n, NoPeriods))
x0 = np.empty(shape=(n, NoPeriods))


# Preallocate space for the portfolio per period value and turnover
currentVal = np.empty(shape=(n))
turnover   = np.empty(shape=(n))
portfValue = np.empty(shape=(NoPeriods*investPeriod))

# Initiate counter for the number of observations per investment period
toDay = 0

# Meaure runtime: start the clock
tic = time.perf_counter()

for t in range(NoPeriods):
  
    # Subset the returns and factor returns corresponding to the current
    # calibration period.
    periodReturns = returns[returns.index <= calEnd]
    periodFactRet = factorRet[factorRet.index <= calEnd]

    priceStart = calEnd - np.timedelta64(1,"M") - np.timedelta64(5,"D")
    currentPrices = adjClose[(adjClose.index >= priceStart) & (adjClose.index <= calEnd)]
    
    # Subset the prices corresponding to the current out-of-sample test 
    # period.
    #periodPrices = table2array( adjClose( testStart <= dates & dates <= testEnd,:) );
    periodPrices = adjClose[(testStart <= dates) & (dates <= testEnd)]

    # Set the initial value of the portfolio or update the portfolio value
    if t == 0:
        currentVal[t] = initialVal
    else:    
        currentVal[t] = (currentPrices @ NoShares.T).values
        # Store the current asset weights (before optimization takes place)
        x0[:,t] = (currentPrices * NoShares) / currentVal[t]

    #----------------------------------------------------------------------
    # Portfolio optimization
    # You must write code your own algorithmic trading function 
    #----------------------------------------------------------------------
    #x(:,t) = Project2_Function(periodReturns, periodFactRet, x0(:,t));

    # Calculate the turnover rate 
    if t > 1:
        turnover[t] = sum( abs( x[:,t] - x0[:,t] ) )
        
    # Number of shares your portfolio holds per stock
    NoShares = x[:,t] * currentVal[t] / currentPrices

    # Update counter for the number of observations per investment period
    fromDay = toDay + 1
    toDay   = toDay + len(periodPrices)

    # Weekly portfolio value during the out-of-sample window
    portfValue[fromDay:toDay] = periodPrices * NoShares

    # # Update your calibration and out-of-sample test periods
    testStart = testStart + np.timedelta64(investPeriod,"M")
    testEnd   = testStart + np.timedelta64(investPeriod,"M") - np.timedelta64(1,"D")
    calEnd    = testStart - np.timedelta64(1,"D")



# Transpose the portfValue into a column vector
portfValue = portfValue.T

# Measure runtime: stop the clock
toc = time.perf_counter()

###########################################################################
## 3. Results
###########################################################################
'''
#--------------------------------------------------------------------------
# 3.1 Calculate the portfolio average return, standard deviation, Sharpe
# ratio and average turnover.
#--------------------------------------------------------------------------

# Calculate the observed portfolio returns
portfRets = portfValue(2:end) ./ portfValue(1:end-1) - 1;

# Calculate the portfolio excess returns
portfExRets = portfRets - table2array(riskFree(dates >= datetime(returns.Properties.RowNames{1}) + calyears(5) + calmonths(1),: ));

# Calculate the portfolio Sharpe ratio 
SR = (geomean(portfExRets + 1) - 1) / std(portfExRets);

# Calculate the average turnover rate
avgTurnover = mean(turnover(2:end));

# Print Sharpe ratio and Avg. turnover to the console
disp(['Sharpe ratio: ', num2str(SR)]);
disp(['Avg. turnover: ', num2str(avgTurnover)]);

#--------------------------------------------------------------------------
# 3.2 Portfolio wealth evolution plot
#--------------------------------------------------------------------------

# Calculate the dates of the out-of-sample period
plotDates = dates(dates >= datetime(returns.Properties.RowNames{1}) + calyears(5) );

fig1 = figure(1);
plot(plotDates, portfValue)

datetick('x','dd-mmm-yyyy','keepticks','keeplimits');
set(gca,'XTickLabelRotation',30);
title('Portfolio wealth evolution', 'FontSize', 14)
ylabel('Total wealth','interpreter','latex','FontSize',12);

# Define the plot size in inches
set(fig1,'Units','Inches', 'Position', [0 0 8, 5]);
pos1 = get(fig1,'Position');
set(fig1,'PaperPositionMode','Auto','PaperUnits','Inches',...
    'PaperSize',[pos1(3), pos1(4)]);

# If you want to save the figure as .pdf for use in LaTeX
# print(fig1,'fileName','-dpdf','-r0');

# If you want to save the figure as .png for use in MS Word
print(fig1,'fileName','-dpng','-r0');

#--------------------------------------------------------------------------
# 3.3 Portfolio weights plot
#--------------------------------------------------------------------------

# Portfolio weights
fig2 = figure(2);
area(x')
legend(tickers, 'Location', 'eastoutside','FontSize',12);
title('Portfolio weights', 'FontSize', 14)
ylabel('Weights','interpreter','latex','FontSize',12);
xlabel('Rebalance period','interpreter','latex','FontSize',12);

# Define the plot size in inches
set(fig2,'Units','Inches', 'Position', [0 0 8, 5]);
pos1 = get(fig2,'Position');
set(fig2,'PaperPositionMode','Auto','PaperUnits','Inches',...
    'PaperSize',[pos1(3), pos1(4)]);

# If you want to save the figure as .pdf for use in LaTeX
# print(fig2,'fileName2','-dpdf','-r0');

# If you want to save the figure as .png for use in MS Word
print(fig2,'fileName2','-dpng','-r0');

###########################################################################
# Program End
'''