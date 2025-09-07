from fastapi import FastAPI, Query
from typing import List, Dict, Any
import yfinance as yf

app = FastAPI()

SELECTED_INFO_FIELDS = [
    "industry", "sector", "fullTimeEmployees", "marketCap", "previousClose",
    "averageVolume", "currency", "dividendRate", "dividendYield", "trailingPE", "forwardPE"
]

@app.get("/extract/{ticker}")
def extract_ticker(
    ticker: str,
    period: str = Query("1mo", description="Period for historical data, e.g. '1mo', '1y', etc.")
) -> Dict[str, Any]:
    t = yf.Ticker(ticker)
    info = t.info
    filtered_info = {k: info.get(k) for k in SELECTED_INFO_FIELDS}
    filtered_info["Ticker"] = ticker
    hist = t.history(period=period)
    hist = hist.reset_index()
    records = []
    for _, row in hist.iterrows():
        record = {
            "Date": row["Date"].strftime("%Y-%m-%d") if hasattr(row["Date"], "strftime") else str(row["Date"]),
            "Open": row.get("Open"),
            "High": row.get("High"),
            "Low": row.get("Low"),
            "Close": row.get("Close"),
            "Volume": row.get("Volume"),
            "Dividend": row.get("Dividends", 0.0),
        }
        record.update(filtered_info)
        records.append(record)
    return {"data": records}

# New endpoint: Only company info fields
@app.get("/info/{ticker}")
def get_info(ticker: str) -> Dict[str, Any]:
    t = yf.Ticker(ticker)
    info = t.info
    filtered_info = {k: info.get(k) for k in SELECTED_INFO_FIELDS}
    filtered_info["Ticker"] = ticker
    return filtered_info

# New endpoint: Only historical OHLCV and dividends
@app.get("/history/{ticker}")
def get_history(
    ticker: str,
    period: str = Query("1mo", description="Period for historical data, e.g. '1mo', '1y', etc.")
) -> Dict[str, Any]:
    t = yf.Ticker(ticker)
    hist = t.history(period=period)
    hist = hist.reset_index()
    records = []
    for _, row in hist.iterrows():
        record = {
            "Date": row["Date"].strftime("%Y-%m-%d") if hasattr(row["Date"], "strftime") else str(row["Date"]),
            "Open": row.get("Open"),
            "High": row.get("High"),
            "Low": row.get("Low"),
            "Close": row.get("Close"),
            "Volume": row.get("Volume"),
            "Dividend": row.get("Dividends", 0.0),
        }
        records.append(record)
    return {"data": records}

# New endpoint: Multiple tickers at once
@app.get("/extract_many")
def extract_many(
    ticker: str = Query(..., description="Comma-separated tickers, e.g. 'AAPL,MSFT'"),
    period: str = Query("1mo", description="Period for historical data, e.g. '1mo', '1y', etc.")
) -> Dict[str, Any]:
    tickers = [t.strip() for t in ticker.split(",") if t.strip()]
    all_data = {}
    for tkr in tickers:
        t = yf.Ticker(tkr)
        info = t.info
        filtered_info = {k: info.get(k) for k in SELECTED_INFO_FIELDS}
        filtered_info["Ticker"] = tkr
        hist = t.history(period=period)
        hist = hist.reset_index()
        records = []
        for _, row in hist.iterrows():
            record = {
                "Date": row["Date"].strftime("%Y-%m-%d") if hasattr(row["Date"], "strftime") else str(row["Date"]),
                "Open": row.get("Open"),
                "High": row.get("High"),
                "Low": row.get("Low"),
                "Close": row.get("Close"),
                "Volume": row.get("Volume"),
                "Dividend": row.get("Dividends", 0.0),
            }
            record.update(filtered_info)
            records.append(record)
        all_data[tkr] = records
    return {"data": all_data}
