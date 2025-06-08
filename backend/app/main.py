from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI(title="Stock Signal API")

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
