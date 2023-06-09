import cvxpy as cvx
import numpy as np

def OLS(returns, factRet):
    
    # Use this function to perform a basic OLS regression with all factors. 
    # You can modify this function (inputs, outputs and code) as much as
    # you need to.
 
    # *************** WRITE YOUR CODE HERE ***************
    #----------------------------------------------------------------------
    
    # Number of observations and factors
    [T, p] = size(factRet) 
    
    # Data matrix
    X = [ones(T,1) factRet]
    
    # Regression coefficients
    B = (X' * X) \ X' * returns
    
    # Separate B into alpha and betas
    a = B(1,:)'     
    V = B(2:end,:) 
    
    # Residual variance
    ep       = returns - X * B
    sigma_ep = 1/(T - p - 1) .* sum(ep .^2, 1)
    D        = diag(sigma_ep)

    # R^2 calculation
    ybar = mean(returns)
    SSR = sum(((X * B) - ybar).^2)
    SST = sum((returns - ybar).^2)
    r2 = 1 - (SSR./SST)
    adj_r2 = mean(1 - ((1-r2)*(T-1)./(T-p-1)))
    
    # Factor expected returns and covariance matrix
    f_bar = mean(factRet,1)'
    F     = cov(factRet)
    
    # Calculate the asset expected returns and covariance matrix
    mu = a + V.T * f_bar
    Q  = V.T * F * V + D
    
    # Sometimes quadprog shows a warning if the covariance matrix is not
    # perfectly symmetric.
    Q = (Q + Q')/2
    return (mu, Q)
    #----------------------------------------------------------------------
    
end