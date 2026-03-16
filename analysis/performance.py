import numpy as np
import pandas as pd


def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["daily_return"] = df["Close"].pct_change()
    df["cumulative_return"] = (1 + df["daily_return"]).cumprod() - 1
    return df


def calculate_metrics(df: pd.DataFrame, ticker_name: str) -> dict:
    df = calculate_returns(df)
    returns = df["daily_return"].dropna()

    total_return = df["cumulative_return"].iloc[-1] * 100

    volatility = returns.std() * np.sqrt(252) * 100

    rolling_max = df["Close"].cummax()
    drawdown = (df["Close"] / rolling_max) - 1
    max_drawdown = drawdown.min() * 100

    avg_return = returns.mean()
    sharpe = (avg_return / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0

    current_price = df["Close"].iloc[-1]
    prev_price = df["Close"].iloc[-2] if len(df) > 1 else current_price
    daily_change = ((current_price / prev_price) - 1) * 100

    return {
        "ticker": ticker_name,
        "current_price": round(current_price, 2),
        "daily_change_pct": round(daily_change, 2),
        "total_return_pct": round(total_return, 2),
        "volatility_pct": round(volatility, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
        "sharpe_ratio": round(sharpe, 2),
        "avg_volume": int(df["Volume"].mean()),
    }


def calculate_correlation(dfs: dict) -> pd.DataFrame:
    returns = pd.DataFrame({
        name: calculate_returns(df)["daily_return"]
        for name, df in dfs.items()
    }).dropna()
    return returns.corr()


def normalized_performance(dfs: dict) -> pd.DataFrame:
    frames = []
    for name, df in dfs.items():
        df = calculate_returns(df).copy()
        df["ticker"] = name
        df["norm"] = (1 + df["daily_return"]).cumprod() * 100
        frames.append(df[["norm", "ticker"]])
    return pd.concat(frames)
