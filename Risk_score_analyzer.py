import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

# Step 1: Define static dataset
cryptocurrency_data = [
    {"name": "Bitcoin", "sentiment_score": 8.5, "smartcontract_score": 9.0, "regulatory_score": 8.0, "active_address_score": 9.0, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
    {"name": "Ethereum", "sentiment_score": 8.2, "smartcontract_score": 8.8, "regulatory_score": 7.5, "active_address_score": 8.5, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
    {"name": "Tether", "sentiment_score": 6.8, "smartcontract_score": 7.0, "regulatory_score": 5.0, "active_address_score": 7.0, "whitepaper_exists": 1, "risk_category": "High Risk - Buy with Caution"},
    {"name": "Binance Coin", "sentiment_score": 7.4, "smartcontract_score": 8.0, "regulatory_score": 6.0, "active_address_score": 7.5, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
    {"name": "Avalanche", "sentiment_score": 7.5, "smartcontract_score": 8.2, "regulatory_score": 6.5, "active_address_score": 7.0, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
    {"name": "Hex", "sentiment_score": 6.5, "smartcontract_score": 7.5, "regulatory_score": 4.5, "active_address_score": 6.0, "whitepaper_exists": 1, "risk_category": "High Risk - Buy with Caution"},
    {"name": "Safemoon", "sentiment_score": 5.0, "smartcontract_score": 4.0, "regulatory_score": 3.0, "active_address_score": 4.0, "whitepaper_exists": 0, "risk_category": "High Risk - Do Not Buy"},
    {"name": "Tron", "sentiment_score": 7.2, "smartcontract_score": 8.0, "regulatory_score": 6.0, "active_address_score": 7.0, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
    {"name": "Verge", "sentiment_score": 5.5, "smartcontract_score": 6.0, "regulatory_score": 4.0, "active_address_score": 5.0, "whitepaper_exists": 1, "risk_category": "High Risk - Buy with Caution"},
    {"name": "BitTorrent", "sentiment_score": 6.7, "smartcontract_score": 7.2, "regulatory_score": 5.5, "active_address_score": 6.5, "whitepaper_exists": 1, "risk_category": "High Risk - Buy with Caution"}
]

# Convert dataset to DataFrame
df = pd.DataFrame(cryptocurrency_data)

# Encode risk categories to numeric labels
df["risk_category"] = df["risk_category"].map({
    "Low Risk - Buy": 2,
    "High Risk - Buy with Caution": 1,
    "High Risk - Do Not Buy": 0
})

# Define features and target
X = df[["sentiment_score", "smartcontract_score", "regulatory_score", "active_address_score", "whitepaper_exists"]]
y = df["risk_category"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Train ML model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Calculate feature importances
feature_importances = model.feature_importances_
feature_names = ["Sentiment Score", "Smart Contract Score", "Regulatory Score", "Active Address Score", "Whitepaper Exists"]
default_weights = {name: round(importance, 2) for name, importance in zip(feature_names, feature_importances)}

# Normalize weights
total_importance = sum(default_weights.values())
normalized_weights = {key: round(value / total_importance, 2) for key, value in default_weights.items()}

# Step 3: Streamlit App for ML-based Risk Analysis
st.title("ML-based Cryptocurrency Risk Analysis with Dynamic Default Weights")

# Display static scores
st.header("Cryptocurrency Scores")
selected_crypto = st.selectbox("Select Cryptocurrency", [crypto["name"] for crypto in cryptocurrency_data])
selected_data = next(crypto for crypto in cryptocurrency_data if crypto["name"] == selected_crypto)

st.write("### Static Scores")
st.write(selected_data)

# Display dynamically determined default weights
st.header("Default Weights from ML")
st.write("These weights are dynamically determined based on the ML model's feature importances.")
st.json(normalized_weights)

# Allow users to adjust weights dynamically
st.sidebar.header("Adjust Weights for Risk Analysis")
sentiment_weight = st.sidebar.slider("Sentiment Weight", 0.0, 1.0, normalized_weights["Sentiment Score"])
smartcontract_weight = st.sidebar.slider("Smart Contract Weight", 0.0, 1.0, normalized_weights["Smart Contract Score"])
regulatory_weight = st.sidebar.slider("Regulatory Weight", 0.0, 1.0, normalized_weights["Regulatory Score"])
active_address_weight = st.sidebar.slider("Active Address Weight", 0.0, 1.0, normalized_weights["Active Address Score"])
whitepaper_weight = st.sidebar.slider("Whitepaper Weight", 0.0, 1.0, normalized_weights["Whitepaper Exists"])

# Normalize custom weights
custom_weights = [sentiment_weight, smartcontract_weight, regulatory_weight, active_address_weight, whitepaper_weight]
total_custom_weights = sum(custom_weights)
normalized_custom_weights = [w / total_custom_weights for w in custom_weights]

# Calculate weighted risk score manually
weighted_score = (
    selected_data["sentiment_score"] * normalized_custom_weights[0] +
    selected_data["smartcontract_score"] * normalized_custom_weights[1] +
    selected_data["regulatory_score"] * normalized_custom_weights[2] +
    selected_data["active_address_score"] * normalized_custom_weights[3] +
    selected_data["whitepaper_exists"] * 10 * normalized_custom_weights[4]
)

# Predict risk category using the ML model
input_data = [[
    selected_data["sentiment_score"],
    selected_data["smartcontract_score"],
    selected_data["regulatory_score"],
    selected_data["active_address_score"],
    selected_data["whitepaper_exists"]
]]
predicted_category = model.predict(input_data)[0]

# Map prediction to category label
risk_category = {0: "High Risk - Do Not Buy", 1: "High Risk - Buy with Caution", 2: "Low Risk - Buy"}

# Display results
st.header("Risk Analysis Results")
st.write(f"### Weighted Risk Score: {round(weighted_score, 2)}")
st.write(f"### ML Predicted Risk Category: {risk_category[predicted_category]}")
