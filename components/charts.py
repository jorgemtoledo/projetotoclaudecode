import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.settings import COLORS


def create_candlestick_chart(df: pd.DataFrame, ticker: str, indicators: list) -> go.Figure:
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.72, 0.28],
        vertical_spacing=0.03,
    )

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"],
        name=ticker,
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350",
    ), row=1, col=1)

    ma_map = {
        "SMA20": ("SMA20", "rgba(255,165,0,0.9)", "dash"),
        "SMA50": ("SMA50", "rgba(173,216,230,0.9)", "dash"),
        "SMA200": ("SMA200", "rgba(238,130,238,0.9)", "dash"),
        "EMA9": ("EMA9", "rgba(255,255,0,0.9)", "dot"),
        "EMA21": ("EMA21", "rgba(144,238,144,0.9)", "dot"),
    }
    for key, (col, color, dash) in ma_map.items():
        if key in indicators and col in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df[col], name=key,
                line=dict(color=color, width=1.2, dash=dash),
            ), row=1, col=1)

    if "Bollinger" in indicators and "BB_upper" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_upper"], name="BB Superior",
            line=dict(color="rgba(200,200,200,0.5)", width=1, dash="dot"),
            showlegend=False,
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_lower"], name="BB Inferior",
            line=dict(color="rgba(200,200,200,0.5)", width=1, dash="dot"),
            fill="tonexty", fillcolor="rgba(200,200,200,0.07)",
        ), row=1, col=1)

    colors_vol = [
        "#26a69a" if row["Close"] >= row["Open"] else "#ef5350"
        for _, row in df.iterrows()
    ]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"],
        name="Volume", marker_color=colors_vol, showlegend=False,
    ), row=2, col=1)

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis2=dict(
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(step="all", label="Tudo"),
                ]
            ),
        ),
    )
    fig.update_yaxes(title_text="Preço (R$)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    return fig


def create_performance_chart(dfs: dict) -> go.Figure:
    fig = go.Figure()
    for name, df in dfs.items():
        norm = (df["Close"] / df["Close"].iloc[0]) * 100
        fig.add_trace(go.Scatter(
            x=df.index, y=norm, name=name,
            line=dict(color=COLORS[name], width=2),
        ))

    fig.add_hline(y=100, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="Base 100")
    fig.update_layout(
        template="plotly_dark",
        height=480,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="Retorno Normalizado (base 100)",
        xaxis_title="Data",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )
    return fig


def create_rsi_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    fig = go.Figure()
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239,83,80,0.12)", line_width=0, annotation_text="Sobrecomprado")
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(38,166,154,0.12)", line_width=0, annotation_text="Sobrevendido")
    fig.add_hline(y=70, line_dash="dash", line_color="rgba(239,83,80,0.5)")
    fig.add_hline(y=30, line_dash="dash", line_color="rgba(38,166,154,0.5)")
    fig.add_trace(go.Scatter(
        x=df.index, y=df["RSI"], name=f"RSI(14) {ticker}",
        line=dict(color=COLORS.get(ticker, "#7fbbe9"), width=1.5),
    ))
    fig.update_layout(
        template="plotly_dark",
        height=300,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="RSI", range=[0, 100]),
        hovermode="x unified",
    )
    return fig


def create_macd_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.5, 0.5], vertical_spacing=0.05)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["MACD"], name="MACD",
        line=dict(color="#7fbbe9", width=1.5),
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["MACD_signal"], name="Sinal",
        line=dict(color="#ff9800", width=1.5, dash="dash"),
    ), row=1, col=1)

    hist_colors = ["#26a69a" if v >= 0 else "#ef5350" for v in df["MACD_hist"]]
    fig.add_trace(go.Bar(
        x=df.index, y=df["MACD_hist"],
        name="Histograma", marker_color=hist_colors,
    ), row=2, col=1)

    fig.update_layout(
        template="plotly_dark",
        height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )
    fig.update_yaxes(title_text="MACD", row=1, col=1)
    fig.update_yaxes(title_text="Histograma", row=2, col=1)
    return fig


def create_correlation_heatmap(corr: pd.DataFrame) -> go.Figure:
    tickers = list(corr.columns)
    z = corr.values
    text = [[f"{v:.2f}" for v in row] for row in z]

    fig = go.Figure(go.Heatmap(
        z=z, x=tickers, y=tickers, text=text, texttemplate="%{text}",
        colorscale="RdYlGn", zmin=-1, zmax=1,
        colorbar=dict(title="Correlação"),
    ))
    fig.update_layout(
        template="plotly_dark",
        height=380,
        margin=dict(l=10, r=10, t=40, b=10),
        title="Correlação entre Retornos Diários",
    )
    return fig
