# Stock Price Visualizer

An interactive stock market visualization dashboard with technical indicators.

## Features

- **16 Popular Stocks**: Apple, Microsoft, Google, Amazon, Tesla, and more
- **Multiple Timeframes**: 1 month to 5 years
- **Chart Types**: Line, Candlestick, Area charts
- **Moving Averages**: 20-day, 50-day, 200-day MA
- **Technical Indicators**: RSI (Relative Strength Index)
- **Stock Comparison**: Compare multiple stocks normalized to % change

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Note

This version uses simulated stock data for demonstration. For real data, install yfinance:

```bash
pip install yfinance
```

Then replace the `generate_stock_data` function with:

```python
import yfinance as yf

def generate_stock_data(ticker, days):
    stock = yf.Ticker(ticker)
    df = stock.history(period=f"{days}d")
    df = df.reset_index()
    df["Date"] = df["Date"].astype(str)
    df = df.rename(columns={"Close": "Close", "Volume": "Volume"})
    return df
```
