from src.factors import compute_momentum, compute_volatility, compute_combined_factors, select_top_stocks
from src.backtest import backtest_portfolio

def main():
    # Factor computation
    momentum_df = compute_momentum()
    volatility_df = compute_volatility()
    combined_df = compute_combined_factors(momentum_df, volatility_df)

    # To this (CORRECT):
    combined_df.sort_values("Composite_score", ascending=True, inplace=True)
    # Select top N
    top_tickers = select_top_stocks(combined_df, top_n=5)
    print("\nTop Portfolio Picks:", top_tickers)

    # Backtest top 5 tickers
    cumulative_returns = backtest_portfolio(top_tickers)
    print("\nCumulative Returns:\n", cumulative_returns.tail())

if __name__ == "__main__":
    main()
