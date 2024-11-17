# main.py

from data_fetching import get_market_data
from data_processing import analyze_sentiment, assess_scam_likelihood
from data_storage import save_data
import time
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def process_symbol(symbol):
    """Processes a given cryptocurrency symbol by fetching data, analyzing it, and saving it locally."""
    try:
        logging.info(f"Starting processing for symbol: {symbol}")

        # Fetch market data
        market_data = get_market_data(symbol)
        if not market_data:
            logging.error(f"No market data found for {symbol}. Aborting processing.")
            print(f"An error occurred while processing {symbol.upper()}. Failed to retrieve market data.")
            return

        time.sleep(1)  # Delay to prevent rate limiting

        # # Fetch news articles
        # news_articles = get_news(symbol)
        # if not news_articles:
        #     logging.error(f"No news articles found for {symbol}. Aborting processing.")
        #     print(f"An error occurred while processing {symbol.upper()}. Failed to retrieve news articles.")
        #     return

        # time.sleep(1)

        # # Extract texts from news articles
        # news_texts = [article['title'] + ' ' + (article.get('description') or '') for article in news_articles]

        # # Analyze sentiments
        # news_sentiments = analyze_sentiment(news_texts)
        # time.sleep(1)

        # # Assess scam likelihood
        # news_scam_scores = assess_scam_likelihood(news_texts)
        # time.sleep(1)

        # Compile data
        data = {
            'symbol': symbol.lower(),
            'market_data': market_data,
            # 'news': news_articles,
            # 'news_sentiments': news_sentiments,
            # 'news_scam_scores': news_scam_scores,
        }

        # Save data locally
        save_data(symbol, data)
        logging.info(f"Processing completed and data saved for symbol: {symbol}")
        print(f"Data for {symbol.upper()} saved successfully.")

    except Exception as e:
        logging.error(f"An error occurred while processing {symbol}: {e}")
        print(f"An error occurred while processing {symbol.upper()}: {e}")

if __name__ == "__main__":
    symbol = input("Enter the cryptocurrency symbol to process (e.g., bitcoin, ethereum): ").strip().lower()
    if symbol:
        process_symbol(symbol)
    else:
        print("No symbol entered. Exiting.")
