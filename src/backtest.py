import pandas as pd
import os

def backtest_portfolio(tickers, data_path="data/raw"):
    prices = pd.DataFrame()

    for ticker in tickers:
        file_path = os.path.join(data_path, f"{ticker}.csv")
        df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
        prices[ticker] = df["Close"]

    # Drop dates where any ticker is missing
    prices.dropna(inplace=True)

    # Calculate daily returns
    returns = prices.pct_change().dropna()

    # Equal-weighted portfolio
    weights = [1 / len(tickers)] * len(tickers)
    portfolio_returns = returns.dot(weights)

    # Calculate cumulative return
    cumulative_returns = (1 + portfolio_returns).cumprod()

    return cumulative_returns
