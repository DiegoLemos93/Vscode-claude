import pandas as pd
import streamlit as st
import yfinance as yf

TICKERS = {
    "Petrobras (PETR4)": "PETR4.SA",
    "Itaú (ITUB4)": "ITUB4.SA",
    "Vale (VALE3)": "VALE3.SA",
}

PERIODS = {
    "1 mês": "1mo",
    "6 meses": "6mo",
    "1 ano": "1y",
    "5 anos": "5y",
}


@st.cache_data(ttl=3600)
def fetch_history(ticker: str, period: str) -> pd.DataFrame:
    return yf.Ticker(ticker).history(period=period)


st.set_page_config(page_title="Ações Brasileiras", page_icon="📈", layout="wide")
st.title("Análise de Ações Brasileiras")
st.caption("Cotações de Petrobras, Itaú e Vale via Yahoo Finance.")

period_label = st.sidebar.selectbox(
    "Período", list(PERIODS.keys()), index=1
)
period = PERIODS[period_label]

data: dict[str, pd.DataFrame] = {}
for name, ticker in TICKERS.items():
    df = fetch_history(ticker, period)
    if df.empty:
        st.error(f"Não foi possível carregar dados de {name} ({ticker}).")
        st.stop()
    data[name] = df

cols = st.columns(3)
for col, (name, df) in zip(cols, data.items()):
    first_close = df["Close"].iloc[0]
    last_close = df["Close"].iloc[-1]
    pct = (last_close / first_close - 1) * 100
    col.metric(
        label=name,
        value=f"R$ {last_close:,.2f}",
        delta=f"{pct:+.2f}% no período",
    )

st.divider()

for name, df in data.items():
    st.subheader(name)
    st.line_chart(df["Close"], height=280)

st.divider()
st.subheader("Comparativo (base 100)")
st.caption(
    "Cada série começa em 100 no início do período, facilitando comparar "
    "a rentabilidade das três ações."
)
comparison = pd.DataFrame(
    {name: df["Close"] / df["Close"].iloc[0] * 100 for name, df in data.items()}
)
st.line_chart(comparison, height=400)
