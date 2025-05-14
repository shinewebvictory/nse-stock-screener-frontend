from fastapi import FastAPI
import yfinance as yf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/screener")
def screener():
    stock_symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
    data = []

    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get("currentPrice", 0)
        
        # Simple signal logic
        signal = "BUY" if price % 2 == 0 else "SELL"

        data.append({
            "name": symbol.replace(".NS", ""),  # Stock name
            "price": round(price, 2),
            "signal": signal
        })

    return data
