import os
import time
import pandas as pd
import yfinance as yf
from config.settings import TICKERS, START_DATE, END_DATE, CACHE_DIR, CACHE_TTL_HOURS


def _cache_path(ticker: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, f"{ticker}_{START_DATE}_{END_DATE}.parquet")


def _cache_valid(path: str) -> bool:
    if not os.path.exists(path):
        return False
    age_hours = (time.time() - os.path.getmtime(path)) / 3600
    return age_hours < CACHE_TTL_HOURS


def get_stock_data(ticker: str, force_refresh: bool = False) -> pd.DataFrame:
    path = _cache_path(ticker)

    if not force_refresh and _cache_valid(path):
        return pd.read_parquet(path)

    try:
        df = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=True, progress=False)
        if df.empty:
            raise ValueError(f"Sem dados para {ticker}")

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
        df.index = pd.to_datetime(df.index)
        df.to_parquet(path)
        return df
    except Exception as e:
        if os.path.exists(path):
            return pd.read_parquet(path)
        raise RuntimeError(f"Falha ao baixar {ticker} e sem cache disponível: {e}")


def load_all_tickers(force_refresh: bool = False) -> dict:
    return {name: get_stock_data(symbol, force_refresh) for name, symbol in TICKERS.items()}
