import streamlit as st
from config.settings import TICKERS


def render_sidebar() -> dict:
    st.sidebar.title("Configurações")

    ticker = st.sidebar.radio("Ação", list(TICKERS.keys()), horizontal=True)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Indicadores")
    indicators = st.sidebar.multiselect(
        "Selecione os indicadores",
        ["SMA20", "SMA50", "SMA200", "EMA9", "EMA21", "Bollinger"],
        default=["SMA20", "SMA50"],
    )

    st.sidebar.markdown("---")
    force_refresh = st.sidebar.button("Atualizar Dados")

    return {"ticker": ticker, "indicators": indicators, "force_refresh": force_refresh}
