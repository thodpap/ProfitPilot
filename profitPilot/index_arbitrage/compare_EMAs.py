import cv2
import pandas as pd
import utils
import matplotlib.pyplot as plt

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def read_data(data_file: str, separator=",", data_column="Close", days=10) -> pd.DataFrame:
    """
    Reads data from a CSV file, calculates EMA for the specified column, and returns the DataFrame.

    Args:
        data_file (str): Path to the CSV file.
        separator (str): Separator used in the CSV file (default: ",").
        data_column (str): Name of the column to calculate EMA on.
        days (int): Number of days for the EMA calculation.

    Returns:
        pd.DataFrame: DataFrame with an additional EMA column.
    """
    # Load the CSV file into a DataFrame
    data = pd.read_csv(data_file, sep=separator)
    
    if data_column not in data.columns:
        raise ValueError(f"Column '{data_column}' not found in the provided data.")
    
    # Compute EMA for the specified column
    data['EMA'] = utils.compute_ema_pandas(data[data_column], days)
    return data

def get_ticker_name_from_file(data_file: str) -> str:
    return data_file.split("_")[0]

def plot_emas(ema_list, ema_names, output_file: str):
    """
    Plot the EMAs using Plotly for interactive visualization and save as an HTML file.

    Args:
        ema_list (list of pd.DataFrame): List of DataFrames containing EMA data.
        ema_names (list of str): List of names for the EMAs.
        output_file (str): Path to save the plot as an HTML file.
    """
    # Create a Plotly figure
    fig = make_subplots(rows=1, cols=1)

    for ema_df, name in zip(ema_list, ema_names):
        fig.add_trace(
            go.Scatter(
                x=ema_df['Datetime'], 
                y=ema_df['EMA'], 
                mode='lines',
                name=name
            )
        )

    # Update layout
    fig.update_layout(
        title="Comparison of EMAs",
        xaxis_title="Date",
        yaxis_title="EMA",
        legend_title="EMA Names",
        template="plotly_white",
        width=900,
        height=600
    )

    # Save as an HTML file
    fig.write_html(output_file)
    print(f"Plot saved to {output_file}")

def main(args):
    # Get All filenames that contain hourly in the current directory and read_data
    import os
    files = [f for f in os.listdir('.') if os.path.isfile(f) and 'hourly' in f]
    ema_list = []
    ema_1_names = []
    for file in files:
        data = read_data(file, data_column=args.data_column, days=args.num_days)
        ema_list.append(data)
        ema_1_names.append(get_ticker_name_from_file(file))
    plot_emas(ema_list, ema_1_names, args.output)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Compare EMAs')
    parser.add_argument('--num-days', dest="num_days", type=int, default=10, help='Number of days')
    parser.add_argument('--data-column', type=str, help='Data column')
    parser.add_argument('--output', type=str, help='Output file')

    args = parser.parse_args()

    main(args)