import requests
import json
import os

def get_all_coins_list():
    url = "https://pro-api.coingecko.com/api/v3/coins/list"
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)  # Create the data folder if it doesn't exist
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        coins_list = response.json()  # Parse the response JSON

        # Write the list to a JSON file in the data folder
        json_file_path = os.path.join(data_folder, "coins_list.json")
        with open(json_file_path, "w") as json_file:
            json.dump(coins_list, json_file, indent=4)
        
        print(f"Coins list successfully saved to {json_file_path}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the coins list: {e}")

# Run the function to fetch and save the list of coins
get_all_coins_list()