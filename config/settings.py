import os

TICKERS = {
    "PETR4": "PETR4.SA",
    "ITUB4": "ITUB4.SA",
    "VALE3": "VALE3.SA",
}

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

COLORS = {
    "PETR4": "#1f77b4",
    "ITUB4": "#ff7f0e",
    "VALE3": "#2ca02c",
}

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cache")
CACHE_TTL_HOURS = 1
