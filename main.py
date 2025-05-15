from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Full Nifty 50 stock symbols
nifty50_symbols = [
    "HEROMOTOCO", "JSWSTEEL", "HCLTECH", "TATAMOTORS", "SHRIRAMFIN",
    "TRENT", "ETERNAL", "TATACONSUM", "GRASIM", "ADANIPORTS",
    "MARUTI", "BAJAJ-AUTO", "ADANIENT", "ULTRACEMCO", "RELIANCE",
    "M&M", "TITAN", "ICICIBANK", "TECHM", "HINDALCO",
    "LT", "SUNPHARMA", "HDFCBANK", "ASIANPAINT", "SBILIFE",
    "JIOFIN", "NESTLEIND", "BHARTIARTL", "TATASTEEL", "BAJAJFINSV",
    "EICHERMOT", "APOLLOHOSP", "TCS", "ITC", "DRREDDY",
    "AXISBANK", "INFY", "BEL", "NTPC", "HDFCLIFE",
    "WIPRO", "BAJFINANCE", "POWERGRID", "COALINDIA", "KOTAKBANK",
    "CIPLA", "ONGC", "HINDUNILVR", "SBIN", "INDUSINDBK"
]

# Dummy signal logic (based on price)
def generate_signal(price):
    return "BUY" if price > 1000 else "SELL"

@app.get("/screener")
def screener():
    data = []
    for symbol in nifty50_symbols:
        try:
            ticker = yf.Ticker(symbol + ".NS")
            info = ticker.history(period="1d")
            if not info.empty:
                latest_price = round(info["Close"].iloc[-1], 2)
                signal = generate_signal(latest_price)
                data.append({
                    "symbol": symbol,
                    "price": latest_price,
                    "signal": signal
                })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return data
