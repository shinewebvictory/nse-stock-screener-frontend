from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import csv

app = FastAPI()

# CORS for frontend access
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
                symbols.append(symbol.strip().upper() + ".NS")
    return symbols

symbols = load_symbols_from_csv()

# Signal logic
def get_signal(price):
    return "BUY" if price % 2 == 0 else "SELL"

@app.get("/screener")
def screener():
    result = []
    try:
        data = yf.download(tickers=" ".join(symbols), period="1d", group_by='ticker', threads=True)
        for symbol in symbols:
            short = symbol.replace(".NS", "")
            try:
                price = data[symbol]["Close"].iloc[-1]
                result.append({
                    "symbol": short,
                    "price": round(price, 2),
                    "signal": get_signal(price)
                })
            except Exception as e:
                print(f"Missing data for {symbol}: {e}")
    except Exception as e:
        print("Error downloading data:", e)
    return result
