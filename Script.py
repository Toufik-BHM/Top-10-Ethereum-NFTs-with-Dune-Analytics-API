from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import os
from dotenv import load_dotenv
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def load_dune_api_key():
    """Load DUNE API key from .env file."""
    load_dotenv("./Dune API Key/dune-api-key.env")
    dune_api_key = os.getenv("DUNE_API_KEY")
    return dune_api_key

def get_dune_client(api_key):
    """Create and return a DuneClient instance."""
    return DuneClient(api_key)

def run_dune_query(client, query_id, start_date, end_date):
    """Run a DUNE query and return the results dataframe."""
    query = QueryBase(
        name="TOP 10 NFT Collections by Volume",
        query_id=query_id,
        params=[
            QueryParameter.date_type(name="Start_Date", value=start_date),
            QueryParameter.date_type(name="End_Date", value=end_date),
        ],
    )
    return client.run_query_dataframe(query)

def get_user_input():
    """Get user input for start date and end date."""
    while True:
        start_date_input = input("Enter start date (YYYY-MM-DD HH:MM:SS): ")
        end_date_input = input("Enter end date (YYYY-MM-DD HH:MM:SS): ")

        try:
            # Autocomplete the time part with "00:00:00" if not provided by the user
            start_date_input = start_date_input + " 00:00:00" if len(start_date_input.split()) == 1 else start_date_input
            end_date_input = end_date_input + " 00:00:00" if len(end_date_input.split()) == 1 else end_date_input
            
            start_date = datetime.strptime(start_date_input, "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(end_date_input, "%Y-%m-%d %H:%M:%S")
            if start_date >= end_date:
                print("Error: End date must be after start date.")
            else:
                return start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S"), start_date.date(), end_date.date()
        except ValueError:
            print("Error: Please enter dates in the correct format (YYYY-MM-DD HH:MM:SS).")

def millions_formatter(x, pos):
    """Formatter function for millions."""
    return f'{x/1e6:.0f}M'

def thousands_formatter(x, pos):
    """Formatter function for thousands."""
    return f'{x/1e3:.0f}K'

def main():
    # Load DUNE API key
    dune_api_key = load_dune_api_key()

    if dune_api_key:
        print("DUNE API key loaded successfully.")
    else:
        print("DUNE API key not found in the .env file.")
        return

    # Create DuneClient instance
    dune_client = get_dune_client(dune_api_key)

    # Get user input for start date and end date
    start_date, end_date, start_date_str, end_date_str = get_user_input()

    # Define query parameters
    query_id = 3546641

    # Run query and get results dataframe
    results_df = run_dune_query(dune_client, query_id, start_date, end_date)

    # Save the dataframe to CSV in the Results folder
    results_folder = './Results'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    results_df.to_csv(os.path.join(results_folder, 'results.csv'), index=False)

    # Visualizations
    sns.set_theme()

    # Plotting USD Volume
    plt.figure(figsize=(10, 6))
    results_df_usd = results_df.sort_values(by='usd_volume', ascending=False)
    sns.barplot(x='usd_volume', y='collection', data=results_df_usd, palette='viridis')
    plt.xlabel('USD Volume')
    plt.ylabel('Collection')
    plt.title(f'Top 10 NFT Collections by USD Volume ({start_date_str} to {end_date_str})')
    plt.gca().xaxis.set_major_formatter(FuncFormatter(millions_formatter))
    plt.show()

    # Plotting ETH Volume
    plt.figure(figsize=(10, 6))
    results_df_eth = results_df.sort_values(by='eth_volume', ascending=False)
    sns.barplot(x='eth_volume', y='collection', data=results_df_eth, palette='magma')
    plt.xlabel('ETH Volume')
    plt.ylabel('Collection')
    plt.title(f'Top 10 NFT Collections by ETH Volume ({start_date_str} to {end_date_str})')
    plt.gca().xaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    plt.show()

if __name__ == "__main__":
    main()