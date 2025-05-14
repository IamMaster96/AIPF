import numpy as np
import requests
import warnings
import os
import urllib3
import pandas as pd
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



ALPHA_VANTAGE_API_KEY = os.getenv("AV_API_KEY")  # Set your API key as an environment variable

def fetch_time_series_data(ticker, start_date, online=True, output_size="compact"):
    """
    Returns a pandas DataFrame with daily time series data (open, close) for a given ticker and start date.
    If online=False, reads from 'ticker_data.csv'.
    """
    if not online:
        try:
            df = pd.read_csv("ticker_data.csv")
            df = df[(df['ticker'] == ticker) & (df['date'] >= start_date)]
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date').reset_index(drop=True)
            return df
        except Exception as e:
            print(f"Failed to read from CSV for {ticker}: {e}")
            return pd.DataFrame()

    if not ALPHA_VANTAGE_API_KEY:
        print("Alpha Vantage API key not set. Please set the AV_API_KEY environment variable.")
        return pd.DataFrame()

    url = (
        "https://www.alphavantage.co/query?"
        "function=TIME_SERIES_DAILY&"
        f"symbol={ticker}&"
        f"outputsize={output_size}&"
        "datatype=json&"
        f"apikey={ALPHA_VANTAGE_API_KEY}"
    )
    try:
        print(f"Fetching data for {ticker} from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        time_series = data.get("Time Series (Daily)", {})
        print(f"Fetched {len(time_series)} records for {ticker}")
        records = []
        for date_str, values in time_series.items():
            if date_str >= start_date:
                records.append({
                    "date": date_str,
                    "open": float(values["1. open"]),
                    "close": float(values["4. close"]),
                    "ticker": ticker
                })
        df = pd.DataFrame(records)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date').reset_index(drop=True)
        return df
    except Exception as e:
        print(f"Failed to fetch time series data for {ticker}: {e}")
        return pd.DataFrame()

# Example tickers
tickers = ["VOO","VOOG","IBIT"]
start_date = "2025-01-01"

# In the future, read tickers from a JSON file
# with open('tickers.json', 'r') as f:
#     tickers = json.load(f)

all_records = pd.DataFrame()
for ticker in tickers:
    data = fetch_time_series_data(ticker, start_date, online=False)
    # If online is False, read from CSV
    all_records = pd.concat([all_records, data], ignore_index=True)   

# Place the full data in a DataFrame
df = pd.DataFrame(all_records)
# Convert date to datetime format
print(df)
