# Stock Signal App

An AI-powered mobile application that helps users make better stock trading decisions based on technical indicators.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Flutter (Dart)
- **Database**: PostgreSQL
- **APIs**: Alpha Vantage / Yahoo Finance

## Features
- User Authentication (JWT)
- Real-time Stock Data Fetching
- Technical Analysis: RSI, MACD, Moving Averages
- Personalized Buy/Sell/Hold Signals
- Portfolio Management

## Getting Started

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/your-username/stock-signal-app.git

# Navigate to the backend
cd stock-signal-app/backend

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI app
uvicorn app:app --reload
