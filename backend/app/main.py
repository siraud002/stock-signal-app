from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

app = FastAPI(title="Stock Signal API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/price/{symbol}")
async def get_price(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            raise ValueError("No data found")
        price = round(float(data["Close"].iloc[-1]), 2)
        return {"symbol": symbol, "price": price}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.get("/signal/{symbol}")
async def get_signal(symbol: str, period: int = 50):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=f"{period*2}d")
        if data.empty:
            raise ValueError("No data found")
        price = round(float(data["Close"].iloc[-1]), 2)
        ma = round(float(data["Close"].rolling(window=period).mean().iloc[-1]), 2)
        signal = "buy" if price > ma else "sell"
        return {"symbol": symbol, "price": price, "moving_average": ma, "signal": signal}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.get("/fetch_stock/{symbol}")
async def fetch_stock(symbol: str, period: int = 50):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=f"{period*2}d")
        if data.empty:
            raise ValueError("No data found")
        price = round(float(data["Close"].iloc[-1]), 2)
        ma = round(float(data["Close"].rolling(window=period).mean().iloc[-1]), 2)
        signal = "buy" if price > ma else "sell"
        return {"symbol": symbol, "price": price, "moving_average": ma, "signal": signal}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.get("/compression_screen")
async def compression_screen():
    """Scan predefined tickers for moving-average compression breakouts."""
    tickers = [
        "AAPL", "MSFT", "GOOG", "AMZN", "META", "TSLA", "NFLX", "NVDA", "ADBE",
        "ORCL", "INTC", "IBM", "CSCO", "QCOM", "TXN", "AMD", "BABA", "NKE", "WMT",
        "HD", "C", "BAC", "JPM", "GS", "MS", "UBER", "LYFT", "SQ", "PYPL", "SHOP",
        "CRM", "WORK", "ZM", "DOCU", "SNOW", "PLTR", "F", "GM", "GE", "T", "VZ",
        "SBUX", "MCD", "KO", "PEP", "PM", "MO", "XOM", "CVX", "BP", "COP",
    ]

    results = []
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="100d")
            if data.empty:
                continue
            close = data["Close"]
            sma20 = close.rolling(window=20).mean().iloc[-1]
            sma35 = close.rolling(window=35).mean().iloc[-1]
            sma50 = close.rolling(window=50).mean().iloc[-1]
            price = close.iloc[-1]

            if pd.isna(sma20) or pd.isna(sma35) or pd.isna(sma50):
                continue
            if not (sma20 > sma35 > sma50):
                continue
            delta1 = abs(sma20 - sma35)
            delta2 = abs(sma35 - sma50)
            if delta1 > 0.03 * sma35 or delta2 > 0.03 * sma50:
                continue

            if "Volume" in data.columns:
                vol_ma20 = data["Volume"].rolling(window=20).mean().iloc[-1]
                if not pd.isna(vol_ma20):
                    if data["Volume"].iloc[-1] < 1.2 * vol_ma20:
                        continue

            results.append(
                {
                    "symbol": symbol,
                    "price": round(float(price), 2),
                    "SMA20": round(float(sma20), 2),
                    "SMA35": round(float(sma35), 2),
                    "SMA50": round(float(sma50), 2),
                    "delta1": round(float(delta1), 2),
                    "delta2": round(float(delta2), 2),
                }
            )
            
@app.get("/fetch_stocks")
async def fetch_stocks(symbols: str, period: int = 50):
    results = []
    for symbol in [s.strip() for s in symbols.split(",") if s.strip()]:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f"{period*2}d")
            if data.empty:
                raise ValueError("No data found")
            price = round(float(data["Close"].iloc[-1]), 2)
            ma = round(float(data["Close"].rolling(window=period).mean().iloc[-1]), 2)
            if price > ma * 1.01:
                signal = "strong buy"
            elif price > ma:
                signal = "buy"
            elif price < ma * 0.99:
                signal = "strong sell"
            else:
                signal = "sell"
            results.append({"symbol": symbol, "price": price, "moving_average": ma, "signal": signal})
        except Exception as exc:
            results.append({"symbol": symbol, "error": str(exc)})
    return results

@app.get("/screen")
async def screen(symbols: str, short_ma: int = 20, long_ma: int = 50):
    """
    Customizable stock screener.

    symbols: comma-separated list of tickers (e.g. AAPL,MSFT,GOOG)
    short_ma: short moving average period (default 20)
    long_ma: long moving average period (default 50)
    """
    results = []
    ticker_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]

    for symbol in ticker_list:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f"{long_ma * 2}d")
            if data.empty:
                continue
            sma_short = data["Close"].rolling(window=short_ma).mean().iloc[-1]
            sma_long = data["Close"].rolling(window=long_ma).mean().iloc[-1]
            if pd.isna(sma_short) or pd.isna(sma_long):
                continue

            price = round(float(data["Close"].iloc[-1]), 2)
            sma_short = round(float(sma_short), 2)
            sma_long = round(float(sma_long), 2)

            signal = "buy" if sma_short > sma_long else "hold"

            results.append({
                "symbol": symbol,
                "price": price,
                "sma_short": sma_short,
                "sma_long": sma_long,
                "signal": signal
            })
        except Exception:
            continue

    return results
