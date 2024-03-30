# Explanation of Script

This script integrates with the Dune Analytics API to retrieve data about the top 10 NFT collections by volume within a specified date range. It prompts the user to input the start and end dates for the query, loads the DUNE API key from a `.env` file, and runs the query using the `dune_client` library. It then displays the results DataFrame and creates visualizations using Seaborn for better data representation.

## Components of the Script

### Loading DUNE API Key
- The `load_dune_api_key()` function loads the DUNE API key from a `.env` file using the `load_dotenv` function from the `dotenv` library.

### Creating DuneClient Instance
- The `get_dune_client(api_key)` function creates and returns a `DuneClient` instance using the provided API key.

### Running DUNE Query
- The `run_dune_query(client, query_id, start_date, end_date)` function runs a DUNE query to retrieve data within the specified date range. It constructs the query using `QueryBase` and `QueryParameter` objects from the `dune_client` library.

### User Input for Date Range
- The `get_user_input()` function prompts the user to input the start and end dates for the query. It validates the input format and ensures that the end date is after the start date.

### Main Function
- The `main()` function serves as the entry point of the script. It orchestrates the execution of other functions, including loading the API key, creating the DuneClient instance, getting user input, running the query, displaying the results DataFrame, and creating visualizations.

### Visualizations
- The script uses Seaborn to create two visualizations:
  1. A horizontal bar plot showing the top 10 NFT collections by USD volume.
  2. A horizontal bar plot showing the top 10 NFT collections by ETH volume.

## Running the Script
- To run the script, execute it using a Python interpreter. Follow the prompts to input the start and end dates for the query.
- Ensure that the required libraries (`dune_client`, `dotenv`, `seaborn`, `matplotlib`) are installed in your Python environment.
