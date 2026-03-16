import streamlit as st
from analysis.performance import calculate_metrics


def render_metrics_row(df, ticker_name: str):
    metrics = calculate_metrics(df, ticker_name)

    cols = st.columns(5)
    cols[0].metric("Preço Atual", f"R$ {metrics['current_price']:.2f}")
    cols[1].metric(
        "Variação Dia",
        f"{metrics['daily_change_pct']:+.2f}%",
        delta=f"{metrics['daily_change_pct']:+.2f}%",
        delta_color="normal",
    )
    cols[2].metric(
        "Retorno 2025",
        f"{metrics['total_return_pct']:+.2f}%",
        delta=f"{metrics['total_return_pct']:+.2f}%",
        delta_color="normal",
    )
    cols[3].metric("Volatilidade Anual", f"{metrics['volatility_pct']:.2f}%")
    cols[4].metric("Drawdown Máx.", f"{metrics['max_drawdown_pct']:.2f}%")
