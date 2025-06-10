from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI(title="Stock Signal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Allow all origins for development; for production, restrict it!
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
        price = float(data["Close"].iloc[-1])
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
        price = float(data["Close"].iloc[-1])
        ma = float(data["Close"].rolling(window=period).mean().iloc[-1])
        signal = "buy" if price > ma else "sell"
        return {"symbol": symbol, "price": price, "moving_average": ma, "signal": signal}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.get("/fetch_stock/{symbol}")
async def fetch_stock(symbol: str, period: int = 50):
    """Return price, moving average and signal in one request."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=f"{period*2}d")
        if data.empty:
            raise ValueError("No data found")
        price = float(data["Close"].iloc[-1])
        ma = float(data["Close"].rolling(window=period).mean().iloc[-1])
        signal = "buy" if price > ma else "sell"
        return {"symbol": symbol, "price": price, "moving_average": ma, "signal": signal}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))
        
@app.get("/fetch_stocks")
async def fetch_stocks(symbols: str, period: int = 50):
    """Return price, moving average and signal for multiple symbols.

    ``symbols`` should be a comma separated list like ``AAPL,MSFT``.
    """
    results = []
    for symbol in [s.strip() for s in symbols.split(",") if s.strip()]:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f"{period*2}d")
            if data.empty:
                raise ValueError("No data found")
            price = float(data["Close"].iloc[-1])
            ma = float(data["Close"].rolling(window=period).mean().iloc[-1])
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
