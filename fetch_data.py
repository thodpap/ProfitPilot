import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_data(symbol, start_date, end_date, interval='1h', chunk_delta=30):
    """
    Fetches hourly stock data for a given symbol within the specified date range.

    Args:
        symbol (str): Stock ticker symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval (default '1h').

    Returns:
        pd.DataFrame: DataFrame containing the hourly stock data.
    """
    # Initialize date range
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    all_data = []

    # Fetch data in chunks (yfinance limitation)
    while start < end:
        chunk_end = start + timedelta(days=chunk_delta)
        if chunk_end > end:
            chunk_end = end

        print(f"Fetching data from {start.strftime('%Y-%m-%d')} to {chunk_end.strftime('%Y-%m-%d')}...")
        data = yf.download(
            symbol,
            start=start.strftime('%Y-%m-%d'),
            end=chunk_end.strftime('%Y-%m-%d'),
            interval=interval
        )

        if not data.empty:
            all_data.append(data)

        start = chunk_end

    # Concatenate all data and reset index
    if all_data:
        full_data = pd.concat(all_data)
        full_data.reset_index(inplace=True)
        return full_data
    else:
        print("No data retrieved.")
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    stock_symbol = 'WMT'
    start = '2023-01-17'
    end = '2024-12-31'
    interval = '1h'

    data = fetch_data(stock_symbol, start, end, interval)

    # Save to CSV
    if not data.empty:
        filename = f"{stock_symbol}_hourly_{start}_to_{end}.csv"
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")
