# YFinance Extraction Service

This service provides a FastAPI-based REST API to extract selected financial data from Yahoo Finance using the yfinance library.

## How to Run

1. Install dependencies:
   ```sh
   pip install fastapi uvicorn yfinance
   ```
2. Start the service:
   ```sh
   uvicorn extract_service:app --reload
   ```
3. The API will be available at `http://127.0.0.1:8000/`

---

## API Endpoints

### 1. Extract All Selected Fields for a Ticker
**GET** `/extract/{ticker}?period=1mo`
- Returns: For each date in the period, a record with:
  - Ticker
  - Date
  - Open
  - High
  - Low
  - Close
  - Volume
  - Dividend
  - industry
  - sector
  - fullTimeEmployees
  - marketCap
  - previousClose
  - averageVolume
  - currency
  - dividendRate
  - dividendYield
  - trailingPE
  - forwardPE

### 2. Company Info Only
**GET** `/info/{ticker}`
- Returns:
  - Ticker
  - industry
  - sector
  - fullTimeEmployees
  - marketCap
  - previousClose
  - averageVolume
  - currency
  - dividendRate
  - dividendYield
  - trailingPE
  - forwardPE

### 3. Historical OHLCV and Dividends Only
**GET** `/history/{ticker}?period=1mo`
- Returns: For each date in the period, a record with:
  - Date
  - Open
  - High
  - Low
  - Close
  - Volume
  - Dividend

### 4. Extract for Multiple Tickers
**GET** `/extract_many?ticker=AAPL,MSFT&period=1mo`
- Returns: For each ticker, a list of records (same as `/extract/{ticker}` endpoint).

---

## Example Usage
- `GET /extract/AAPL?period=1mo`
- `GET /info/GOOG`
- `GET /history/TSLA?period=6mo`
- `GET /extract_many?ticker=AAPL,MSFT&period=1y`

---

## Common Ticker Symbols
You can use any valid Yahoo Finance ticker symbol. Here are some common examples:

| Ticker | Company Name           |
|--------|------------------------|
| AAPL   | Apple Inc.             |
| MSFT   | Microsoft Corp.        |
| TSLA   | Tesla Inc.             |
| GOOG   | Alphabet Inc. (Google) |
| AMZN   | Amazon.com Inc.        |
| META   | Meta Platforms (Facebook) |
| NFLX   | Netflix Inc.           |
| NVDA   | NVIDIA Corp.           |
| JPM    | JPMorgan Chase & Co.   |
| BRK-B  | Berkshire Hathaway     |
| V      | Visa Inc.              |
| DIS    | Walt Disney Co.        |
| BAC    | Bank of America        |
| WMT    | Walmart Inc.           |
| UNH    | UnitedHealth Group     |

You can find more tickers on [Yahoo Finance](https://finance.yahoo.com/lookup/).

---

## Notes
- The `period` query parameter can be any valid yfinance period (e.g., `1d`, `5d`, `1mo`, `6mo`, `1y`, etc.).
- All responses are in JSON format.
- Only the specified fields are included in the output for clarity and efficiency.


<!-- eaaedf15-564f-4d27-879b-311d1b329c9c
16ceedfe-ed43-4a5a-ba60-1338e5dfc455 -->