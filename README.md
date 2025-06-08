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

## Frontend Setup (Flutter)

### Prerequisites
- [Flutter SDK](https://flutter.dev/docs/get-started/install)
- Android Studio / VSCode (with Flutter extensions)

### Setup Instructions
```bash
# Navigate to the frontend directory
cd stock-signal-app/frontend

# Get Flutter dependencies
flutter pub get

# Connect a physical device or start an emulator

# Run the Flutter app
flutter run
```


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
The backend exposes two simple endpoints:

- `/price/{symbol}` – return the latest closing price for `symbol`.
- `/signal/{symbol}` – compute a basic moving-average signal for `symbol`.

