# data_processing.py

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import openai
import re
import logging
import time

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def clean_text(text):
    """Cleans the input text by removing special characters and extra whitespace."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove unwanted characters
    return text.strip()

def truncate_text(text, max_length=2000):
    """Truncates the text to a maximum number of characters."""
    return text[:max_length] if len(text) > max_length else text

def prepare_prompt_sentiment(text):
    """Prepares the prompt for sentiment analysis."""
    return (
        f"Analyze the sentiment of the following text and classify it as Positive, Negative, or Neutral.\n\n"
        f"Text: \"{text}\"\n\nSentiment:"
    )

def prepare_prompt_scam(text):
    """Prepares the prompt for scam likelihood assessment."""
    return (
        f"Based on the following text, assess the likelihood of it being related to a scam on a scale from 0 to 10 "
        f"(0 = not a scam, 10 = definitely a scam).\n\nText: \"{text}\"\n\nScam Likelihood Score:"
    )

def call_openai_api(prompt, max_tokens=10, model="gpt-3.5-turbo", max_retries=3, backoff_factor=2):
    """Calls the OpenAI API with retries for transient errors."""
    retries = 0
    while retries < max_retries:
        try:
            logging.info(f"Calling OpenAI API with prompt: {prompt[:50]}...")
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=max_tokens,
                n=1,
                stop=None,
            )
            if response and 'choices' in response and len(response.choices) > 0:
                result = response.choices[0].message['content'].strip()
                logging.info(f"OpenAI API response: {result[:50]}...")
                return result
            else:
                logging.warning("Unexpected API response structure.")
                return None
        except openai.error.RateLimitError as e:
            logging.warning(f"Rate limit reached. Retrying in {backoff_factor ** retries} seconds...")
            time.sleep(backoff_factor ** retries)
            retries += 1
        except openai.error.APIConnectionError as e:
            logging.warning(f"API connection error. Retrying in {backoff_factor ** retries} seconds...")
            time.sleep(backoff_factor ** retries)
            retries += 1
        except openai.error.InvalidRequestError as e:
            logging.error(f"Invalid request: {e}")
            return None
        except openai.error.AuthenticationError as e:
            logging.error(f"Authentication error: {e}")
            return None
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None
    logging.error("Max retries exceeded for OpenAI API call.")
    return None

def analyze_sentiment(texts):
    """Analyzes sentiment of given texts using OpenAI's GPT models."""
    sentiments = []
    for text in texts:
        clean = clean_text(text)
        clean = truncate_text(clean)
        prompt = prepare_prompt_sentiment(clean)
        sentiment = call_openai_api(prompt, max_tokens=10)
        if sentiment:
            # Ensure sentiment is one of the expected classes
            if sentiment.lower() in ["positive", "negative", "neutral"]:
                sentiments.append(sentiment.capitalize())
                logging.info(f"Sentiment analysis successful for text: {text[:50]}...")
            else:
                sentiments.append("Neutral")  # Default sentiment
                logging.warning(f"Unexpected sentiment result for text: {text[:50]} - Sentiment: {sentiment}")
        else:
            sentiments.append("Neutral")
            logging.warning(f"Sentiment analysis returned empty or failed for text: {text[:50]}...")
    return sentiments

def assess_scam_likelihood(texts):
    """Assesses scam likelihood of given texts using OpenAI's GPT models."""
    assessments = []
    for text in texts:
        clean = clean_text(text)
        clean = truncate_text(clean)
        prompt = prepare_prompt_scam(clean)
        score = call_openai_api(prompt, max_tokens=5)
        # Validate score
        if score and score.isdigit() and 0 <= int(score) <= 10:
            assessments.append(score)
            logging.info(f"Scam assessment successful for text: {text[:50]} - Score: {score}")
        else:
            assessments.append("N/A")
            logging.warning(f"Scam assessment returned invalid score for text: {text[:50]} - Score: {score}")
    return assessments

def prepare_market_dataframe(market_data_list):
    """Converts a list of market data dictionaries into a pandas DataFrame."""
    df = pd.DataFrame(market_data_list)
    return df

def calculate_indicators(df):
    """Calculates additional indicators for the market data DataFrame."""
    df['price_change_percentage'] = df['price_change_percentage_24h']
    df['volume_change_percentage'] = df['total_volume'].pct_change() * 100
    return df

def calculate_volatility(price_series):
    """Calculates annualized volatility from a price series."""
    returns = price_series.pct_change()
    volatility = returns.std() * np.sqrt(365)  # Annualized volatility
    return volatility
