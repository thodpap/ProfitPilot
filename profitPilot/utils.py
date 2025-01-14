import pandas as pd

def compute_ema_pandas(data, num_days, normalize=True):
    """
    Compute the Exponential Moving Average (EMA) for a given period using Pandas.

    Args:
        column (pd.Series): The target column containing numerical data (e.g., closing prices).
        num_days (int): The number of days for the EMA.

    Returns:
        pd.Series: A Series containing the EMA values.
    """
    if not isinstance(data, pd.Series):
        raise TypeError("Input column must be a Pandas Series.")
    
    if num_days <= 0:
        raise ValueError("num_days must be greater than 0.")
    
    if normalize:
        data = normalize_column_min_max(data)

    # Use Pandas' `ewm` method to compute EMA
    ema = data.ewm(span=num_days, adjust=False).mean()
    return ema


def normalize_column_min_max(column):
    """
    Normalize a Pandas Series using Min-Max normalization (0-1 scaling).

    Args:
        column (pd.Series): The target column containing numerical data.

    Returns:
        pd.Series: A normalized column with values scaled between 0 and 1.
    """
    if not isinstance(column, pd.Series):
        raise TypeError("Input must be a Pandas Series.")
    
    min_val = column.min()
    max_val = column.max()
    
    if min_val == max_val:
        raise ValueError("Cannot normalize a column with constant values.")
    
    normalized = (column - min_val) / (max_val - min_val)
    return normalized