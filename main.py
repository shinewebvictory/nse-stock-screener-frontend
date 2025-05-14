from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

nse_stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]

def get_signal(price: float) -> str:
    return "BUY" if price % 2 == 0 else "SELL"

@app.get("/screener")
def screener():
    results = []
    for symbol in nse_stocks:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            continue
        price = round(data["Close"][-1], 2)
        signal = get_signal(price)
        results.append({
            "symbol": symbol.replace(".NS", ""),
            "price": price,
            "signal": signal
        })
    return results
