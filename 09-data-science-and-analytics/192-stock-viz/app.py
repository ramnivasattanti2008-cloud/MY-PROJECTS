import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Stock Price Visualizer", page_icon="📈", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #ffffff !important; }
    .stock-up { color: #4ade80; }
    .stock-down { color: #ef4444; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Stock Price Visualizer")
st.markdown("Track stock prices with moving averages and technical indicators")

# Popular stocks
STOCKS = {
    "Apple": "AAPL", "Microsoft": "MSFT", "Google": "GOOGL", "Amazon": "AMZN",
    "Tesla": "TSLA", "Meta": "META", "NVIDIA": "NVDA", "Netflix": "NFLX",
    "Intel": "INTC", "AMD": "AMD", "Goldman Sachs": "GS", "JPMorgan": "JPM",
    "Disney": "DIS", "Nike": "NKE", "McDonald's": "MCD", "Coca-Cola": "KO"
}

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    selected_stock = st.selectbox("Select Stock", list(STOCKS.keys()))
with col2:
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
with col3:
    chart_type = st.selectbox("Chart Type", ["Line", "Candlestick", "Area"])

# Period mapping
PERIOD_DAYS = {"1mo": 30, "3mo": 90, "6mo": 180, "1y": 365, "2y": 730, "5y": 1825}

# Generate realistic stock data
def generate_stock_data(ticker, days):
    end_date = datetime.now()

    # Base prices per ticker
    BASE_PRICES = {"AAPL": 180, "MSFT": 380, "GOOGL": 140, "AMZN": 180, "TSLA": 250,
                   "META": 350, "NVDA": 480, "NFLX": 450, "INTC": 45, "AMD": 150,
                   "GS": 380, "JPM": 170, "DIS": 95, "NKE": 100, "MCD": 280, "KO": 60}

    base_price = BASE_PRICES.get(ticker, 100)

    random.seed(hash(ticker) % 1000)

    dates = [(end_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days, -1, -1)]

    data = []
    price = base_price * random.uniform(0.7, 1.3)
    volatility = random.uniform(0.02, 0.04)

    for date in dates:
        change = random.gauss(0.0005, volatility)
        price = max(price * (1 + change), 1)

        high = price * random.uniform(1.01, 1.05)
        low = price * random.uniform(0.95, 0.99)
        open_price = random.uniform(low, high)
        close = price

        data.append({
            "Date": date,
            "Open": round(open_price, 2),
            "High": round(high, 2),
            "Low": round(low, 2),
            "Close": round(close, 2),
            "Volume": random.randint(10000000, 100000000)
        })

    return pd.DataFrame(data)

# Get data
ticker = STOCKS[selected_stock]
days = PERIOD_DAYS[period]
df = generate_stock_data(ticker, days)

# Calculate moving averages
df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()
df["MA200"] = df["Close"].rolling(window=200).mean()

# Calculate RSI
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df["RSI"] = calculate_rsi(df["Close"])

# Latest price metrics
latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest
price_change = latest["Close"] - prev["Close"]
price_change_pct = (price_change / prev["Close"]) * 100

# Display metrics
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(f"{selected_stock} ({ticker})", f"${latest['Close']:.2f}",
            f"{price_change_pct:+.2f}%")
col2.metric("Open", f"${latest['Open']:.2f}")
col3.metric("High", f"${latest['High']:.2f}")
col4.metric("Low", f"${latest['Low']:.2f}")
col5.metric("Volume", f"{latest['Volume']/1000000:.1f}M")

# Charts
st.markdown("---")
tab1, tab2, tab3, tab4 = st.tabs(["📈 Price Chart", "📊 Volume", "📉 Technical Indicators", "🔄 Comparison"])

with tab1:
    if chart_type == "Line":
        fig = px.line(df, x="Date", y=["Close", "MA20", "MA50", "MA200"],
                     title=f"{selected_stock} Stock Price",
                     labels={"value": "Price ($)", "Date": "Date", "variable": "Indicator"})
        fig.update_layout(template="plotly_dark", height=600, legend_title_text="")
    elif chart_type == "Area":
        fig = px.area(df, x="Date", y="Close", title=f"{selected_stock} Stock Price")
        fig.update_layout(template="plotly_dark", height=600)
        fig.update_yaxes(title_text="Price ($)")
    else:
        fig = go.Figure(data=[go.Candlestick(x=df["Date"], open=df["Open"],
                                             high=df["High"], low=df["Low"],
                                             close=df["Close"], name="OHLC")])
        fig.update_layout(template="plotly_dark", height=600, title=f"{selected_stock} Candlestick")

    fig.update_xaxes(title_text="Date")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.bar(df, x="Date", y="Volume", title="Trading Volume",
                 color_discrete_sequence=["#00d4ff"])
    fig.update_layout(template="plotly_dark", height=500)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Volume")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # RSI chart
    fig = px.line(df, x="Date", y="RSI", title="Relative Strength Index (RSI)",
                  color_discrete_sequence=["#f97316"])
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
    fig.update_layout(template="plotly_dark", height=400)
    fig.update_yaxes(title_text="RSI", range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    # Price with MA
    fig2 = px.line(df, x="Date", y=["Close", "MA20", "MA50"],
                   title="Price with Moving Averages")
    fig2.update_layout(template="plotly_dark", height=400, legend_title_text="")
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    # Compare multiple stocks
    compare_stocks = st.multiselect("Compare with",
                                    [s for s in STOCKS.keys() if s != selected_stock],
                                    default=["Apple", "Microsoft"])

    if compare_stocks:
        fig = go.Figure()
        for stock in [selected_stock] + compare_stocks:
            t = STOCKS[stock]
            data = generate_stock_data(t, min(days, 365))
            # Normalize to percentage change
            start_price = data["Close"].iloc[0]
            pct_change = ((data["Close"] - start_price) / start_price) * 100
            fig.add_trace(go.Scatter(x=data["Date"], y=pct_change,
                                     name=stock, mode="lines"))

        fig.update_layout(template="plotly_dark", height=600,
                        title="Normalized Price Comparison (% Change)",
                        yaxis_title="% Change")
        st.plotly_chart(fig, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📋 Recent Price Data")
st.dataframe(df.tail(20).sort_values("Date", ascending=False),
            use_container_width=True)

st.caption("Data powered by Yahoo Finance simulation | For demonstration purposes")
