import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Ações Brasil 2025",
    page_icon="📈",
    layout="wide",
)

from components.sidebar import render_sidebar
from components.metrics_cards import render_metrics_row
from components.charts import (
    create_candlestick_chart,
    create_performance_chart,
    create_rsi_chart,
    create_macd_chart,
    create_correlation_heatmap,
)
from analysis.indicators import add_all_indicators
from analysis.performance import calculate_correlation
from data.fetcher import load_all_tickers


@st.cache_data(ttl=3600, show_spinner=False)
def cached_load(force: bool = False):
    return load_all_tickers(force_refresh=force)


config = render_sidebar()

st.title("📈 Dashboard de Ações — 2025")
st.caption("Petrobras (PETR4) · Itaú (ITUB4) · Vale (VALE3)")

with st.spinner("Carregando dados..."):
    try:
        all_data = cached_load(force=config["force_refresh"])
        if config["force_refresh"]:
            st.cache_data.clear()
            all_data = cached_load(force=False)
    except RuntimeError as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.stop()

ticker = config["ticker"]
df_raw = all_data[ticker]
df = add_all_indicators(df_raw)

st.subheader(f"{ticker} — Métricas Rápidas")
render_metrics_row(df_raw, ticker)

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Candlestick",
    "📉 Análise Técnica",
    "🏆 Performance Comparativa",
    "🔗 Correlação",
    "🗂️ Dados Brutos",
])

with tab1:
    st.subheader(f"Gráfico de Candlestick — {ticker}")
    fig = create_candlestick_chart(df, ticker, config["indicators"])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader(f"Indicadores Técnicos — {ticker}")
    st.markdown("**RSI (14 períodos)**")
    st.plotly_chart(create_rsi_chart(df, ticker), use_container_width=True)
    st.markdown("**MACD (12, 26, 9)**")
    st.plotly_chart(create_macd_chart(df, ticker), use_container_width=True)

with tab3:
    st.subheader("Performance Comparativa — PETR4 vs ITUB4 vs VALE3")
    st.caption("Retorno normalizado (base 100 = primeiro pregão de 2025)")
    fig_perf = create_performance_chart(all_data)
    st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown("**Resumo de Retornos**")
    from analysis.performance import calculate_metrics
    summary = [calculate_metrics(all_data[t], t) for t in all_data]
    df_summary = pd.DataFrame([{
        "Ação": m["ticker"],
        "Preço Atual (R$)": m["current_price"],
        "Retorno 2025 (%)": m["total_return_pct"],
        "Volatilidade (%)": m["volatility_pct"],
        "Drawdown Máx. (%)": m["max_drawdown_pct"],
        "Sharpe Ratio": m["sharpe_ratio"],
    } for m in summary])
    st.dataframe(df_summary.set_index("Ação"), use_container_width=True)

with tab4:
    st.subheader("Correlação entre Retornos Diários")
    corr = calculate_correlation(all_data)
    st.plotly_chart(create_correlation_heatmap(corr), use_container_width=True)
    st.caption("Valores próximos de 1 indicam alta correlação positiva; próximos de -1, correlação negativa.")

with tab5:
    st.subheader(f"Dados Brutos — {ticker}")
    display_df = df_raw.copy()
    display_df.index = display_df.index.strftime("%Y-%m-%d")
    display_df = display_df.rename(columns={
        "Open": "Abertura", "High": "Máximo",
        "Low": "Mínimo", "Close": "Fechamento", "Volume": "Volume",
    })
    st.dataframe(display_df.style.format({
        "Abertura": "R$ {:.2f}", "Máximo": "R$ {:.2f}",
        "Mínimo": "R$ {:.2f}", "Fechamento": "R$ {:.2f}",
        "Volume": "{:,.0f}",
    }), use_container_width=True, height=450)

    csv = display_df.to_csv().encode("utf-8")
    st.download_button(
        label="⬇️ Baixar CSV",
        data=csv,
        file_name=f"{ticker}_2025.csv",
        mime="text/csv",
    )
