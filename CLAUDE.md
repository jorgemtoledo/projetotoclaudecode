# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

There are no test files or lint configuration in this project.

## Architecture

Brazilian stock market analysis dashboard (PETR4, ITUB4, VALE3) built with Streamlit.

**Data flow:**
1. `app.py` — entry point; orchestrates all layers and renders 5 tabs
2. `data/fetcher.py` — downloads from Yahoo Finance via yfinance, caches as Parquet with 1-hour TTL in `data/cache/`
3. `analysis/indicators.py` — computes SMA (20/50/200), EMA (9/21), RSI (14), Bollinger Bands, MACD on raw DataFrames
4. `analysis/performance.py` — computes returns, volatility, Sharpe ratio, drawdown, and correlation matrix
5. `components/` — Streamlit/Plotly UI: `sidebar.py` (controls), `charts.py` (all Plotly figures), `metrics_cards.py` (KPI row)

**Key config:** `config/settings.py` defines tickers (`.SA` suffix for B3), date range (2025), colors, and cache path.

**Data shape:** `fetcher.py` flattens MultiIndex columns from yfinance downloads. `indicators.py` appends columns to the same DataFrame. Each ticker's data is stored and processed independently.

## GitHub Repository

**Repositório:** https://github.com/jorgemtoledo/projetotoclaudecode

**Auto-sync está configurado:** toda vez que Claude edita um arquivo, um commit e push são feitos automaticamente via hook `PostToolUse` em `~/.claude/settings.json`.

Para sincronizar mudanças manuais (fora do Claude Code), rode em um terminal separado:

```bash
./auto_sync.sh
```

Esse script verifica mudanças a cada 30 segundos e faz commit+push automaticamente.

**Comandos git úteis:**
```bash
git status          # ver mudanças pendentes
git log --oneline   # ver histórico de commits
git push origin main  # push manual se necessário
```

## Tab Layout (app.py)

| Tab | Content |
|-----|---------|
| Preço & Indicadores | Candlestick + overlaid SMA/EMA/BB + volume |
| Osciladores | RSI + MACD subplots |
| Performance | Normalized cumulative return comparison + metrics table |
| Correlação | Heatmap of pairwise daily return correlations |
| Dados | Raw data table + CSV download |
