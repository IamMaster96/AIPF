import numpy as np
import requests
import warnings
import os
import urllib3
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
# Suppress warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

output_size="compact"

ALPHA_VANTAGE_API_KEY = os.getenv("AV_API_KEY") # Set your API key as an environment variable

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
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return data
    except Exception as e:
        print(f"Failed to fetch time series data for {ticker}: {e}")
        return None

# Example tickers
tickers = ["VOO"]
start_date = "2025-05-01"

# In the future, read tickers from a JSON file
# with open('tickers.json', 'r') as f:
#     tickers = json.load(f)

for ticker in tickers:
    data = fetch_time_series_data(ticker, start_date)
    print(f"{ticker} time series data since {start_date}:")
    if data:
        for entry in data:
            print(entry)
    else:
        print("No data available.")