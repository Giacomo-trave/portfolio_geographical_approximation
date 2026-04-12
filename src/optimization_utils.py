import pandas as pd
import numpy as np 
from scipy.optimize import minimize

def compute_optimal_weights(df_etf):
    #compute the best allocation for SWDA and XMME to match VWCE 
    # Define optimization problem and find the optimal weights using a standard optimization algorithm

    alpha, beta, gamma = df_etf['SWDA'], df_etf['XMME'], df_etf['VWCE']
    history = []

    def objective(vars):
        x, y = vars
        val = np.linalg.norm(alpha * x + beta * y - gamma)**2
        return val

    def callback(xk):
        # Calculate the function value at the current iteration's coordinates
        score = objective(xk)
        history.append(score)
        print(f"Iteration {len(history)}: {score}")

    x0 = [0.5, 0.5]
    constraints = ({'type': 'eq', 'fun': lambda x: x[0] + x[1] - 1})

    res = minimize(objective, x0, method='SLSQP', callback=callback, constraints=constraints, options={'maxiter': 5000, 'disp': True})
    optimal_weights = res.x

    return optimal_weights