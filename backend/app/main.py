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

