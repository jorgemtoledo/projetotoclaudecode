import numpy as np
import pandas as pd


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()
    df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
    df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()
    return df


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = df.copy()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df


def add_bollinger_bands(df: pd.DataFrame, period: int = 20, std: int = 2) -> pd.DataFrame:
    df = df.copy()
    sma = df["Close"].rolling(period).mean()
    rolling_std = df["Close"].rolling(period).std()
    df["BB_upper"] = sma + std * rolling_std
    df["BB_middle"] = sma
    df["BB_lower"] = sma - std * rolling_std
    return df


def add_macd(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_hist"] = df["MACD"] - df["MACD_signal"]
    return df


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_bollinger_bands(df)
    df = add_macd(df)
    return df
