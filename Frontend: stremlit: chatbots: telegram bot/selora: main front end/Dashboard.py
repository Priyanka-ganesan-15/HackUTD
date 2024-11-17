import pandas as pd
import streamlit as st
import requests
import json
from typing import Dict, Optional

def fetch_data(crypto: str) -> Optional[Dict]:
    """Fetch data for a specific cryptocurrency from the API."""
    url = f'http://localhost:8000/apis/home?crypto={crypto}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data for {crypto}: {str(e)}")
        
        return None

# def fetch_all_crypto_data(cryptocurrency_list: list) -> Dict:
#     """Fetch data for all cryptocurrencies."""
#     all_data = {}
#     with st.spinner("Fetching cryptocurrency data..."):
#         for crypto in cryptocurrency_list:
#             result = fetch_data(crypto)
#             if result is not None:
#                 all_data[crypto] = result
#     return all_data

def get_risk_category(score: float) -> str:
    """Determine risk category based on weighted score."""
    if score >= 8:
        return "Very Low Risk"
    elif score >= 6:
        return "Low Risk"
    elif score >= 4:
        return "Medium Risk"
    elif score >= 2:
        return "High Risk"
    else:
        return "Very High Risk"

# List of cryptocurrencies
cryptocurrency_list = [
    "Bitcoin", "Ethereum", "Tether", "Binance Coin", "Avalanche",
    "Hex", "Safemoon", "Tron", "Verge", "BitTorrent"
]

# Streamlit App
st.title("ML-based Cryptocurrency Risk Analysis Using API Weights")

# Initialize or get data store
# if 'data_store' not in st.session_state:
#     st.session_state.data_store = fetch_all_crypto_data(cryptocurrency_list)

# Select Cryptocurrency
st.header("Select Cryptocurrency")
selected_crypto = st.selectbox("Select Cryptocurrency", cryptocurrency_list, index=0)

# Get data for selected cryptocurrency from storage
result = fetch_data(selected_crypto)
print(result)
if result is not None:
    # Parse the 'body' key
    body = json.loads(result.get('message').get('body', '{}'))

    # Extract weights and metrics
    weights = body.get('weights')
    crypto_metrics = body.get('cryptoCurrencyMetrics')
    print('Data:', weights, crypto_metrics)
    # Ensure all necessary data is available
    if not weights or not crypto_metrics:
        print("still go")
        st.error("Incomplete data received from the API.")
    else:
        with st.container():
        # Add a header with an icon
            st.markdown(f"## :rocket: {crypto_metrics['name']} ({crypto_metrics['symbol']})")
            
            # Add a separator
            st.markdown("---")

            # Create columns for the metrics
            col1, col2 = st.columns(2)

            with col1:
                st.metric(label="Sentiment Score", value=crypto_metrics['sentiment_score'])
                st.metric(label="Regulatory Score", value=crypto_metrics['regulatory_score'])
                whitepaper_status = "Yes" if crypto_metrics['whitepaper_exists'] == 1 else "No"
                st.write(f"**Whitepaper Exists:** {whitepaper_status}")
            with col2:
                st.metric(label="Smart Contract Score", value=crypto_metrics['smartcontract_score'])
                st.metric(label="Active Address Score", value=crypto_metrics['active_address_score'])
                # Display the risk category using Streamlit status elements
                risk_category = crypto_metrics['risk_category']
                if risk_category == "Low Risk - Buy":
                    st.success(f"Risk Category: {risk_category}")
                elif risk_category == "High Risk - Do Not Buy":
                    st.error(f"Risk Category: {risk_category}")
                else:
                    st.warning(f"Risk Category: {risk_category}")

            # Add another separator
            st.markdown("---")

        # Move sliders to main page
        st.header("Adjust Weights for Risk Analysis")
        col1, col2 = st.columns(2)

        with col1:
            sentiment_weight = st.slider(
                "Sentiment Weight", 0.0, 2.0, weights.get("Sentiment Score", 0.2)
            )
            smartcontract_weight = st.slider(
                "Smart Contract Weight", 0.0, 2.0, weights.get("Smart Contract Score", 0.2)
            )
            regulatory_weight = st.slider(
                "Regulatory Weight", 0.0, 2.0, weights.get("Regulatory Score", 0.2)
            )

        with col2:
            active_address_weight = st.slider(
                "Active Address Weight", 0.0, 2.0, weights.get("Active Address Score", 0.2)
            )
            whitepaper_weight = st.slider(
                "Whitepaper Weight", 0.0, 2.0, weights.get("Whitepaper Exists", 0.2)
            )

        # Normalize custom weights
        custom_weights = [
            sentiment_weight, smartcontract_weight, regulatory_weight,
            active_address_weight, whitepaper_weight
        ]
        total_custom_weights = sum(custom_weights)
        normalized_custom_weights = [w / total_custom_weights for w in custom_weights]

        # Get scores from crypto_metrics
        sentiment_score = crypto_metrics.get("sentiment_score", 0)
        smartcontract_score = crypto_metrics.get("smartcontract_score", 0)
        regulatory_score = crypto_metrics.get("regulatory_score", 0)
        active_address_score = crypto_metrics.get("active_address_score", 0)
        whitepaper_exists = crypto_metrics.get("whitepaper_exists", 0)

        # Calculate weighted risk score
        weighted_score = (
            sentiment_score * normalized_custom_weights[0] +
            smartcontract_score * normalized_custom_weights[1] +
            regulatory_score * normalized_custom_weights[2] +
            active_address_score * normalized_custom_weights[3] +
            whitepaper_exists * 10 * normalized_custom_weights[4]
        )

        # Get risk category based on weighted score
        risk_category = get_risk_category(weighted_score)

        # Display results
        st.header("Risk Analysis Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Weighted Risk Score", f"{weighted_score:.2f}")
        with col2:
            st.metric("Risk Category", risk_category)

        # Display individual scores
        st.subheader("Individual Scores")
        scores_df = pd.DataFrame({
            'Metric': ['Sentiment', 'Smart Contract', 'Regulatory', 'Active Address', 'Whitepaper'],
            'Raw Score': [sentiment_score, smartcontract_score, regulatory_score, 
                         active_address_score, whitepaper_exists],
            'Weight': normalized_custom_weights,
            'Weighted Score': [
                sentiment_score * normalized_custom_weights[0],
                smartcontract_score * normalized_custom_weights[1],
                regulatory_score * normalized_custom_weights[2],
                active_address_score * normalized_custom_weights[3],
                whitepaper_exists * 10 * normalized_custom_weights[4]
            ]
        })
        st.dataframe(scores_df)

else:
    st.error("Failed to fetch data for the selected cryptocurrency.")