from fastapi import FastAPI
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from datetime import datetime


app = FastAPI()


class Record(BaseModel):
    Date: Optional[str] = Field(None, description="Date in ISO format")
    Open: Optional[float]
    High: Optional[float]
    Low: Optional[float]
    Close: Optional[float]
    Volume: Optional[int]
    Dividend: Optional[float]
    industry: Optional[str]
    sector: Optional[str]
    fullTimeEmployees: Optional[int]
    marketCap: Optional[float]
    previousClose: Optional[float]
    averageVolume: Optional[float]
    currency: Optional[str]
    dividendRate: Optional[float]
    dividendYield: Optional[float]
    trailingPE: Optional[float]
    forwardPE: Optional[float]
    Ticker: Optional[str]


class TransformRequest(BaseModel):
    batch_id: Optional[str] = Field(None, description="Idempotency key for the batch")
    data: List[Record]
    # Optionally, add more fields for config/rules


class TransformResponse(BaseModel):
    batch_id: Optional[str] = Field(None, description="Idempotency key for the batch")
    data: List[Dict[str, Any]]
    errors: List[str]

@app.post("/transform", response_model=TransformResponse)
def transform_data(request: TransformRequest) -> TransformResponse:

    # Load data into DataFrame
    df = pd.DataFrame([r.dict() for r in request.data])

    # --- CLEAN ---
    # Remove duplicates
    df = df.drop_duplicates()

    # Improved null cleaning: fill numeric with 0, string with '', and drop rows with critical nulls
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    string_cols = df.select_dtypes(include=[object]).columns.tolist()
    # Fill numeric columns with 0
    df[numeric_cols] = df[numeric_cols].fillna(0)
    # Fill string columns with ''
    df[string_cols] = df[string_cols].fillna("")
    # Drop rows where critical columns are missing (e.g., Date, Close, Ticker)
    critical_cols = [col for col in ['Date', 'Close', 'Ticker'] if col in df.columns]
    df = df.dropna(subset=critical_cols)
    # Standardize date format and normalize to UTC
    if 'Date' in df.columns:
        # Parse as datetime, localize if naive, convert to UTC, then format as ISO
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        if df['Date'].dt.tz is None:
            df['Date'] = df['Date'].dt.tz_localize('UTC')
        else:
            df['Date'] = df['Date'].dt.tz_convert('UTC')
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    # Standardize currency (example: remove $)
    if 'currency' in df.columns:
        df['currency'] = df['currency'].str.replace('$', '', regex=False)
    # Standardize symbols (example: uppercase)
    if 'Ticker' in df.columns:
        df['Ticker'] = df['Ticker'].str.upper()

    # --- VALIDATE ---
    errors = []
    # Row-level validation: collect errors for each row
    for idx, row in df.iterrows():
        row_errors = []
        if 'Close' in row and (not isinstance(row['Close'], (int, float)) or pd.isnull(row['Close'])):
            row_errors.append(f"Row {idx}: Close price must be numeric and not null")
        if 'Volume' in row and (row['Volume'] < 0 or pd.isnull(row['Volume'])):
            row_errors.append(f"Row {idx}: Volume must be >= 0 and not null")
        if 'Date' in row and (not isinstance(row['Date'], str) or row['Date'] == ""):
            row_errors.append(f"Row {idx}: Date must be present and a string")
        if 'Ticker' in row and (not isinstance(row['Ticker'], str) or row['Ticker'] == ""):
            row_errors.append(f"Row {idx}: Ticker must be present and a string")
        if row_errors:
            errors.extend(row_errors)


    # (No enrichment or reshaping applied)

    # Return transformed data and errors, with batch_id passthrough
    return TransformResponse(batch_id=request.batch_id, data=df.to_dict(orient="records"), errors=errors)
