# 📈 Stock Signal App

An AI-powered web application that helps users make better stock trading decisions based on technical indicators.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React (JavaScript)
- **Database**: PostgreSQL
- **APIs**: Alpha Vantage / Yahoo Finance

## Features
- User Authentication (JWT)
- Real-time Stock Data Fetching
- Technical Analysis: RSI, MACD, Moving Averages
- Personalized Buy/Sell/Hold Signals
- Portfolio Management

## Frontend Setup (React)

### Prerequisites
- [Node.js](https://nodejs.org/) with npm

### Setup Instructions
Open `frontend/index.html` in a browser. It loads the React app from `frontend/src/App.jsx`. Enter one or more symbols separated by commas to query the `/fetch_stocks` endpoint. For local API calls, ensure the FastAPI server is running on `http://localhost:8000`.
---

## 🚀 Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React (JavaScript, Vite)
- **APIs**: Yahoo Finance (via `yfinance`)

---

## 🔥 Features
- Real-time Stock Data Fetching
- Technical Analysis: Moving Averages
- Personalized Buy/Sell Signals

---

## 🛠️ Getting Started

### Backend Setup
### Prerequisites
- [Node.js](https://nodejs.org/) with npm
- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)

---

### 🚧 Backend Setup (FastAPI)

```bash
# Navigate to the backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the FastAPI app
uvicorn app.main:app --reload
```

## Backend API
The backend exposes these endpoints:

- `/price/{symbol}` – return the latest closing price for `symbol`.
- `/signal/{symbol}` – compute a basic moving-average signal for `symbol`.
- `/fetch_stock/{symbol}` – return price, moving average and signal in one response.
- `/fetch_stocks?symbols=AAPL,MSFT` – return price, moving average and signal for multiple symbols at once.
- `/screen?short_ma=20&long_ma=50` – screen built-in tickers for a bullish moving-average crossover.

- `/price/{symbol}` – return the latest closing price for `symbol`.
- `/signal/{symbol}` – compute a basic moving-average signal for `symbol`.
- `/fetch_stock/{symbol}` – return price, moving average and signal in one response.
- `/fetch_stocks?symbols=AAPL,MSFT` – return price, moving average and signal for multiple symbols at once.

uvicorn main:app --reload
```
### 🎨 Frontend Setup (React + Vite)

```bash
# Navigate to the frontend
cd frontend

# Install Node dependencies
npm install

# Start the React development server
npm run dev
```
