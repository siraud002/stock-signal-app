# Stock Signal App

An AI-powered mobile application that helps users make better stock trading decisions based on technical indicators.

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


## Getting Started

### Backend Setup
```bash
# Navigate to the backend
cd stock-signal-app/backend

# Install dependencies
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

