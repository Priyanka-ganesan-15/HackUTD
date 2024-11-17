# data_storage.py

import json
import os
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

DATA_DIR = 'data'

def save_data(symbol, data):
    """Saves the data dictionary to a JSON file named after the symbol."""
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logging.info(f"Created data directory at {DATA_DIR}")
        file_path = os.path.join(DATA_DIR, f"{symbol.lower()}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data for {symbol} saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving data for {symbol}: {e}")

def load_data(symbol):
    """Loads the data dictionary from a JSON file named after the symbol."""
    try:
        file_path = os.path.join(DATA_DIR, f"{symbol.lower()}.json")
        if not os.path.exists(file_path):
            logging.warning(f"Data file for {symbol} does not exist at {file_path}")
            return None
        with open(file_path, 'r') as f:
            data = json.load(f)
        logging.info(f"Data for {symbol} loaded from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error loading data for {symbol}: {e}")
        return None
