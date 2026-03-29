# Crypto Portfolio Tracker API

## Crypto Portfolio Tracker is a backend application designed to manage and analyze a user's cryptocurrency portfolio. It provides functionality for tracking assets, executing buy/sell operations, calculating portfolio value, and analyzing profit and loss (PnL) based on real-time or stored market data. This project is built as a RESTful API and can serve as the backend for web or mobile applications.

## Tech Stack
 - FastAPI
 - SQLAlchemy (Async)
 - PostgreSQL
 - Pydantic
 - Alembic (database migrations)
 - JWT Authentication

## Future Improvements
 - Realized and unrealized PnL
 - Price alerts
 - Background jobs for price updates
 - Market data caching
 - WebSocket support for real-time updates
 - Advanced analytics (best trade, worst trade)

## Getting Started
# Activate virtual environment
```
python -m venv venv
./venv/Scripts/activate
```
# Install dependencies
```
pip install -r requirements.txt
```
# Run the application
```
python -m src.app.main
```

