import os
import pandas as pd

def compute_momentum(data_path="data/raw", lookback_days=252):
    momentum_scores = {}

    for filename in os.listdir(data_path):
        if filename.endswith(".csv"):
            ticker = filename.replace(".csv", "")
            df = pd.read_csv(os.path.join(data_path, filename), parse_dates=["Date"], index_col="Date")

            # Skip if not enough data
            if len(df) < lookback_days:
                continue

            try:
                price_today = df["Close"].iloc[-1]
                price_past = df["Close"].iloc[-lookback_days]
                momentum = (price_today / price_past) - 1
                momentum_scores[ticker] = momentum
            except Exception as e:
                print(f"Skipping {ticker}: {e}")

    # Convert to DataFrame and rank
    momentum_df = pd.DataFrame.from_dict(momentum_scores, orient="index", columns=["Momentum"])
    momentum_df.sort_values("Momentum", ascending=False, inplace=True)

    return momentum_df

def compute_volatility(data_path="data/raw", window=21):
    volatility_scores = {}

    for filename in os.listdir(data_path):
        if filename.endswith(".csv"):
            ticker = filename.replace(".csv", "")
            df = pd.read_csv(os.path.join(data_path, filename), parse_dates=["Date"], index_col="Date")

            try:
                # Calculate daily returns
                df["returns"] = df["Close"].pct_change()

                # Calculate rolling std dev of daily returns (volatility)
                volatility = df["returns"].rolling(window).std().iloc[-1]

                if pd.notnull(volatility):
                    volatility_scores[ticker] = volatility
            except Exception as e:
                print(f"Skipping {ticker}: {e}")

    # Convert to DataFrame and rank ascending (low vol = better if you're risk averse)
    vol_df = pd.DataFrame.from_dict(volatility_scores, orient="index", columns=["Volatility"])
    vol_df.sort_values("Volatility", ascending=True, inplace=True)

    return vol_df


def compute_combined_factors(momentum_df, volatility_df, momentum_weight=0.5, volatility_weight=0.5):
    # Merge both factor scores
    combined_df = momentum_df.join(volatility_df, how="inner")

    # Normalize each column
    combined_df["Momentum_score"] = combined_df["Momentum"].rank(ascending=False)
    combined_df["Volatility_score"] = combined_df["Volatility"].rank(ascending=True)

    # Weighted sum of normalized scores
    combined_df["Composite_score"] = (
        momentum_weight * combined_df["Momentum_score"] +
        volatility_weight * combined_df["Volatility_score"]
    )

    # Final ranking
    combined_df.sort_values("Composite_score", ascending=False, inplace=True)

    return combined_df


def select_top_stocks(combined_df, top_n=5):
    return combined_df.head(top_n).index.tolist()
