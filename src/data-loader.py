import yfinance as yf
import pandas as pd
import os


def download_multiple_stocks(tickers, start="2022-01-01", end="2022-12-31", save_path="data/raw"):
    # Create folder if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Download all at once using yfinance
    data = yf.download(
        tickers,
        start=start,
        end=end,
        group_by="ticker",
        auto_adjust=True,
        threads=True
    )

    for ticker in tickers:
        df = data[ticker].copy()
        df.dropna(inplace=True)
        df.to_csv(f"{save_path}/{ticker}.csv")
        print(f"Saved {ticker} to {save_path}/{ticker}.csv")

if __name__ == "__main__":
    tickers = ["JPM", "BAC", "C", "WFC", "GS", "MS", "USB", "PNC", "TFC", "COF", "BPOP"]
    download_multiple_stocks(tickers)
