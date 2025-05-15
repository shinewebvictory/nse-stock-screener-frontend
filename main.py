from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import csv

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load stock symbols from CSV
def load_symbols_from_csv():
    symbols = []
    with open("9cfe4e90-8a67-4e08-889e-067ff9b05205.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row.get("symbol") or row.get("Symbol") or list(row.values())[0]
            if symbol:
                symbols.append(symbol.strip() + ".NS")
    return symbols

symbols = load_symbols_from_csv()

# Generate signal (simple placeholder logic)
def get_signal(price):
    return "BUY" if price % 2 == 0 else "SELL"

@app.get("/screener")
def screener():
    result = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.history(period="1d")["Close"].iloc[-1]
            result.append({
                "symbol": symbol.replace(".NS", ""),
                "price": round(price, 2),
                "signal": get_signal(price)
            })
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    return result
