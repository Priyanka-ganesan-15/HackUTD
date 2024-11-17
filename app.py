# app.py

import streamlit as st
import pandas as pd
from data_fetching import get_supported_coins, get_market_data
from data_processing import analyze_sentiment, assess_scam_likelihood
from data_storage import save_data, load_data
import time
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Streamlit caching for performance optimization
@st.cache_data(ttl=3600)
def get_coingecko_symbols():
    """Fetches and returns a list of verified CoinGecko symbols."""
    supported_coins = get_supported_coins()
    # Create a list of tuples: (display_name, id)
    # Display name can include name and symbol for clarity
    coins = [(f"{coin['name']} ({coin['symbol'].upper()})", coin['id']) for coin in supported_coins]
    logging.info(f"Fetched {len(coins)} supported coins from CoinGecko.")
    return coins

@st.cache_data(ttl=600)
def get_market_data_cached(symbol):
    return get_market_data(symbol)

@st.cache_data(ttl=600)
def get_news_cached(symbol):
    return get_news(symbol)

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Cryptocurrency Analyzer", layout="wide")
    st.title("🔍 Cryptocurrency Analyzer")
    st.markdown("Analyze the top cryptocurrencies and assess sentiment and scam likelihood based on recent news.")

    # Display top 5 cryptocurrencies
    st.header("📈 Top 5 Cryptocurrencies")
    display_top_cryptocurrencies()

    # Sidebar for selecting a cryptocurrency
    st.sidebar.header("🔍 Analyze Cryptocurrency")
    coins = get_coingecko_symbols()
    # Unzip display names and ids
    display_names, coin_ids = zip(*coins)
    selected_index = st.sidebar.selectbox("Select a cryptocurrency:", range(len(display_names)), format_func=lambda x: display_names[x])
    selected_symbol = coin_ids[selected_index]

    if st.sidebar.button("Analyze"):
        display_symbol_data(selected_symbol)

def display_top_cryptocurrencies():
    """Displays the top 5 cryptocurrencies with current price and 24h change."""
    # Fetch top 5 coins by market cap
    top_symbols = ['bitcoin', 'ethereum', 'tether', 'binancecoin', 'ripple']
    market_data_list = []
    for sym in top_symbols:
        data = get_market_data_cached(sym)
        if data:
            market_data_list.append(data)
        else:
            st.warning(f"Market data for {sym.capitalize()} is unavailable.")
        time.sleep(1.2)  # Delay to avoid rate limiting

    if not market_data_list:
        st.error("No market data available for the top cryptocurrencies.")
        return

    # Create DataFrame
    df = pd.DataFrame(market_data_list)
    df = df[['name', 'current_price', 'price_change_percentage_24h']]
    df.rename(columns={
        'name': 'Name',
        'current_price': 'Current Price (USD)',
        'price_change_percentage_24h': '24h Change (%)'
    }, inplace=True)

    # Format price and percentage
    df['Current Price (USD)'] = df['Current Price (USD)'].apply(lambda x: f"${x:,.2f}")
    df['24h Change (%)'] = df['24h Change (%)'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")

    # Display table
    st.table(df)

def display_symbol_data(symbol):
    """Displays data and analysis for a given cryptocurrency symbol."""
    data = load_data(symbol)
    if not data:
        with st.spinner('Fetching and processing data...'):
            process_and_save(symbol)
            data = load_data(symbol)
        if not data:
            st.error(f"Failed to retrieve data for {symbol.upper()}.")
            return

    # Display Market Data
    st.header(f"📊 Market Data for {data['market_data']['name']}")
    market_data = data['market_data']
    market_info = {
        "Current Price (USD)": f"${market_data['current_price']:,.2f}",
        "Market Cap": f"${market_data['market_cap']:,.2f}",
        "24h Volume": f"${market_data['total_volume']:,.2f}",
        "24h Price Change": f"{market_data['price_change_percentage_24h']:.2f}%",
        "All-Time High": f"${market_data['ath']:,.2f} ({market_data['ath_change_percentage']:.2f}%)",
        "All-Time Low": f"${market_data['atl']:,.2f} ({market_data['atl_change_percentage']:.2f}%)",
    }
    st.json(market_info)

    # Display News Sentiments
    st.header("🗞️ Sentiment Analysis of Recent News")
    news_sentiments = data.get('news_sentiments', [])
    if news_sentiments:
        sentiments_df = pd.DataFrame({
            "Article": [f"Article {i+1}" for i in range(len(news_sentiments))],
            "Sentiment": news_sentiments
        })
        st.table(sentiments_df)
    else:
        st.write("No sentiment data available.")

    # Display Scam Likelihood Assessments
    st.header("⚠️ Scam Likelihood Assessments")
    news_scam_scores = data.get('news_scam_scores', [])
    if news_scam_scores:
        scam_df = pd.DataFrame({
            "Article": [f"Article {i+1}" for i in range(len(news_scam_scores))],
            "Scam Likelihood Score": news_scam_scores
        })
        st.table(scam_df)
    else:
        st.write("No scam likelihood data available.")

def process_and_save(symbol):
    """Processes data for a given symbol and saves it."""
    from data_fetching import get_market_data, get_news
    from data_processing import analyze_sentiment, assess_scam_likelihood
    from data_storage import save_data

    try:
        # Fetch market data
        market_data = get_market_data(symbol)
        if not market_data:
            st.error(f"No market data found for {symbol.upper()}.")
            return

        # Fetch news articles
        news_articles = get_news(symbol)
        if not news_articles:
            st.error(f"No news articles found for {symbol.upper()}.")
            return

        # Extract texts from news articles
        news_texts = [article['title'] + ' ' + (article.get('description') or '') for article in news_articles]

        # Analyze sentiments
        news_sentiments = analyze_sentiment(news_texts)
        time.sleep(1)  # Delay to respect API rate limits

        # Assess scam likelihood
        news_scam_scores = assess_scam_likelihood(news_texts)
        time.sleep(1)

        # Compile data
        data = {
            'symbol': symbol.lower(),
            'market_data': market_data,
            'news': news_articles,
            'news_sentiments': news_sentiments,
            'news_scam_scores': news_scam_scores,
        }

        # Save data
        save_data(symbol, data)
        st.success(f"Data for {market_data['name']} processed and saved successfully.")

    except Exception as e:
        logging.error(f"Error processing symbol {symbol}: {e}")
        st.error(f"An error occurred while processing {symbol.upper()}.")

if __name__ == "__main__":
    main()
