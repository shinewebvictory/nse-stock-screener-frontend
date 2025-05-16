from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
from ta.momentum import StochasticOscillator
from ta.trend import EMAIndicator

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nifty 50 stocks
nifty_50_stocks = [
    "HEROMOTOCO", "JSWSTEEL", "HCLTECH", "TATAMOTORS", "SHRIRAMFIN", "TRENT", "ETERNAL",
    "TATACONSUM", "GRASIM", "ADANIPORTS", "MARUTI", "BAJAJ-AUTO", "ADANIENT", "ULTRACEMCO",
    "RELIANCE", "M&M", "TITAN", "ICICIBANK", "TECHM", "HINDALCO", "LT", "SUNPHARMA", "HDFCBANK",
    "ASIANPAINT", "SBILIFE", "JIOFIN", "NESTLEIND", "BHARTIARTL", "TATASTEEL", "BAJAJFINSV",
    "EICHERMOT", "APOLLOHOSP", "TCS", "ITC", "DRREDDY", "AXISBANK", "INFY", "BEL", "NTPC",
    "HDFCLIFE", "WIPRO", "BAJFINANCE", "POWERGRID", "COALINDIA", "KOTAKBANK", "CIPLA", "ONGC",
    "HINDUNILVR", "SBIN", "INDUSINDBK"
]

def calculate_indicators(symbol):
    try:
        data = yf.Ticker(f"{symbol}.NS").history(period="6mo", interval="1d")
        if data.empty or len(data) < 200:
            return None

        stoch = StochasticOscillator(close=data["Close"], high=data["High"], low=data["Low"], window=14, smooth_window=3)
        data["stoch_k"] = stoch.stoch()
        data["stoch_d"] = stoch.stoch_signal()

        ema_100 = EMAIndicator(close=data["Close"], window=100)
        ema_200 = EMAIndicator(close=data["Close"], window=200)
        data["ema_100"] = ema_100.ema_indicator()
        data["ema_200"] = ema_200.ema_indicator()

        latest = data.iloc[-1]
        price = latest["Close"]
        signal = "HOLD"
        if latest["stoch_k"] > latest["stoch_d"] and price > latest["ema_100"]:
            signal = "BUY"
        elif latest["stoch_k"] < latest["stoch_d"] and price < latest["ema_100"]:
            signal = "SELL"

        return {
            "symbol": symbol,
            "price": round(price, 2),
            "volume": int(latest["Volume"]),
            "stoch_k": round(latest["stoch_k"], 2),
            "stoch_d": round(latest["stoch_d"], 2),
            "ema_100": round(latest["ema_100"], 2),
            "ema_200": round(latest["ema_200"], 2),
            "signal": signal
        }

    except Exception as e:
        print(f"Error for {symbol}: {e}")
        return None

@app.get("/screener")
def screener():
    result = [calculate_indicators(symbol) for symbol in nifty_50_stocks]
    return [r for r in result if r]
