import pandas as pd
import yfinance
from fastapi.testclient import TestClient
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.app.main import app

class DummyTicker:
    def history(self, period="1d"):
        return pd.DataFrame({"Close": [100, 110]})

def _patch_yfinance(monkeypatch):
    monkeypatch.setattr(yfinance, "Ticker", lambda symbol: DummyTicker())

def test_get_price(monkeypatch):
    _patch_yfinance(monkeypatch)
    client = TestClient(app)
    res = client.get("/price/TEST")
    assert res.status_code == 200
    assert res.json()["price"] == 110

def test_get_signal(monkeypatch):
    _patch_yfinance(monkeypatch)
    client = TestClient(app)
    res = client.get("/signal/TEST?period=1")
    assert res.status_code == 200
    assert res.json()["signal"] in {"buy", "sell"}


def test_fetch_stock(monkeypatch):
    _patch_yfinance(monkeypatch)
    client = TestClient(app)
    res = client.get("/fetch_stock/TEST?period=1")
    assert res.status_code == 200
    data = res.json()
    assert data["price"] == 110
    assert "moving_average" in data
    assert data["signal"] in {"buy", "sell"}

class DummyTickerCompression:
    def __init__(self, symbol):
        self.symbol = symbol

    def history(self, period="100d"):
        if self.symbol == "AAPL":
            close = [100] * 50 + [101] * 30 + [102] * 20
            volume = [1000] * 99 + [2000]
            return pd.DataFrame({"Close": close, "Volume": volume})
        return pd.DataFrame({"Close": [100] * 100, "Volume": [1000] * 100})


def _patch_yfinance_compression(monkeypatch):
    monkeypatch.setattr(yfinance, "Ticker", lambda symbol: DummyTickerCompression(symbol))


def test_compression_screen(monkeypatch):
    _patch_yfinance_compression(monkeypatch)
    client = TestClient(app)
    res = client.get("/compression_screen")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    aapl = next((x for x in data if x["symbol"] == "AAPL"), None)
    assert aapl is not None
    assert aapl["price"] == 102.0
    assert aapl["SMA20"] == 102.0
    assert aapl["SMA35"] == 101.57
    assert aapl["SMA50"] == 101.4
    assert aapl["delta1"] == 0.43
    assert aapl["delta2"] == 0.17

def test_fetch_stocks(monkeypatch):
    _patch_yfinance(monkeypatch)
    client = TestClient(app)
    res = client.get("/fetch_stocks?symbols=AAA,BBB&period=1")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert len(items) == 2
    for item in items:
        assert item["price"] == 110
        assert "moving_average" in item
        assert item["signal"] in {"buy", "sell", "strong buy", "strong sell"}

def test_screen(monkeypatch):
    _patch_yfinance(monkeypatch)
    client = TestClient(app)
    res = client.get("/screen?short_ma=1&long_ma=2")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert len(items) == 4
    for item in items:
        assert item["signal"] == "buy"
        assert item["price"] == 110
        assert "sma_short" in item
        assert "sma_long" in item
    res = client.get("/signal/TEST?period=1")
