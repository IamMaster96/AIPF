import numpy as np
import requests
import warnings
import os
import urllib3
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
# Suppress warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
print("Suppressing warnings")
output_size = "compact"

ALPHA_VANTAGE_API_KEY = os.getenv("AV_API_KEY")  # Set your API key as an environment variable

def fetch_time_series_data(ticker, start_date):
    """
    Fetches daily time series data (open, close) from Alpha Vantage API for a given ticker and start date.
    """
    if not ALPHA_VANTAGE_API_KEY:
        print("Alpha Vantage API key not set. Please set the ALPHA_VANTAGE_API_KEY environment variable.")
        return None

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
        # Filter and format data
        records = []
        print(f"Fetched {len(time_series)} records for {ticker}")
        for date_str, values in time_series.items():
            if date_str >= start_date:
                records.append({
                    "date": date_str,
                    "open": float(values["1. open"]),
                    "close": float(values["4. close"]),
                    "ticker": ticker
                })
        return records
    except Exception as e:
        print(f"Failed to fetch time series data for {ticker}: {e}")
        return None

# Example tickers
tickers = ["VOO"]
start_date = "2025-05-01"

# In the future, read tickers from a JSON file
# with open('tickers.json', 'r') as f:
#     tickers = json.load(f)

all_records = []
for ticker in tickers:
    data = fetch_time_series_data(ticker, start_date)
    if data:
        all_records.extend(data)

# Place the full data in a DataFrame
df = pd.DataFrame(all_records)
print(df)