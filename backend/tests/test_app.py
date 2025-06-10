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
