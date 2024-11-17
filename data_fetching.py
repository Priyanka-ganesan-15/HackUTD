# data_fetching.py

import os
import requests
import logging
from dotenv import load_dotenv
import time

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

symbol = [{"bitcoin","btc"}]
# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
COINGECKO_API_URL = os.getenv('COINGECKO_API_URL', 'https://api.coingecko.com/api/v3')
NEWS_API_URL = os.getenv('NEWS_API_URL', 'https://newsapi.org/v2/everything')

def get_supported_coins():
    """Fetches a list of supported coins from CoinGecko API."""
    try:
        logging.info("Fetching supported coins from CoinGecko.")
        url = f"{COINGECKO_API_URL}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 250,  # Maximum per page
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h',
        }
        all_coins = []
        while True:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            all_coins.extend(data)
            params['page'] += 1
            time.sleep(1)  # Delay to respect rate limits
        logging.info(f"Total supported coins fetched: {len(all_coins)}")
        return all_coins
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching supported coins: {e}")
        return []

def get_market_data(symbol):
    """Fetches market data for a given cryptocurrency symbol from CoinGecko API."""
    try:
        logging.info(f"Fetching market data for symbol: {symbol}")
        url = f"{COINGECKO_API_URL}/coins/markets"
        params = {
            'vs_currency': 'usd',
            # 'ids': symbol.lower(),
            'ids': symbol.lower(),
            'order': 'market_cap_desc',
            'per_page': 1,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h',
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            logging.info(f"Market data retrieved for symbol: {symbol}")
            return data[0]
        else:
            logging.warning(f"No market data found for symbol: {symbol}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching market data for {symbol}: {e}")
        return None

# def get_news(symbol, page_size=10):
#     """Fetches news articles for a given cryptocurrency symbol from NewsAPI."""
#     try:
#         logging.info(f"Fetching news articles for symbol: {symbol}")
#         url = NEWS_API_URL
#         params = {
#             'q': 'crypto',
#             'apiKey': NEWS_API_KEY,
#             'language': 'en',
#             'pageSize': page_size,
#             'sortBy': 'publishedAt',
#         }
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         if data['status'] == 'ok':
#             logging.info(f"News articles retrieved for symbol: {symbol}")
#             return data['articles']
#         else:
#             logging.warning(f"NewsAPI returned status: {data['status']} for symbol: {symbol}")
#             return []
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Error fetching news for {symbol}: {e}")
#         return []
