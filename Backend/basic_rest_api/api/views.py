from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Create your views here.

@api_view(['GET'])
def home_view(req):
    cryptoCurr = req.GET.get('crypto')
    def analyze(cryptoCurr):
        # Step 1: Define static dataset
        cryptocurrency_data = [
            {"symbol":"BTC","name": "Bitcoin", "sentiment_score": 8.5, "smartcontract_score": 9.0, "regulatory_score": 8.0, "active_address_score": 9.0, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
            {"symbol":"ETH","name": "Ethereum", "sentiment_score": 8.2, "smartcontract_score": 8.8, "regulatory_score": 7.5, "active_address_score": 8.5, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
            {"symbol":"USDT","name": "Tether", "sentiment_score": 6.8, "smartcontract_score": 7.0, "regulatory_score": 5.0, "active_address_score": 7.0, "whitepaper_exists": 1, "risk_category": "High Risk - Buy with Caution"},
            {"symbol":"BNB","name": "Binance Coin", "sentiment_score": 7.4, "smartcontract_score": 8.0, "regulatory_score": 6.0, "active_address_score": 7.5, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
            {"symbol":"AVAX","name": "Avalanche", "sentiment_score": 7.5, "smartcontract_score": 8.2, "regulatory_score": 6.5, "active_address_score": 7.0, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
            {"symbol":"HEX","name": "Hex", "sentiment_score": 6.5, "smartcontract_score": 7.5, "regulatory_score": 4.5, "active_address_score": 6.0, "whitepaper_exists": 1, "risk_category": "High Risk - Buy with Caution"},
            {"symbol":"SFM","name": "Safemoon", "sentiment_score": 5.0, "smartcontract_score": 4.0, "regulatory_score": 3.0, "active_address_score": 4.0, "whitepaper_exists": 0, "risk_category": "High Risk - Do Not Buy"},
            {"symbol":"TRX","name": "Tron", "sentiment_score": 7.2, "smartcontract_score": 8.0, "regulatory_score": 6.0, "active_address_score": 7.0, "whitepaper_exists": 1, "risk_category": "Low Risk - Buy"},
            {"symbol":"XVG","name": "Verge", "sentiment_score": 5.5, "smartcontract_score": 6.0, "regulatory_score": 4.0, "active_address_score": 5.0, "whitepaper_exists": 1, "risk_category": "High Risk - Buy with Caution"},
            {"symbol":"BTT","name": "BitTorrent", "sentiment_score": 6.7, "smartcontract_score": 7.2, "regulatory_score": 5.5, "active_address_score": 6.5, "whitepaper_exists": 1, "risk_category": "High Risk - Buy with Caution"},
        ]

        cryptoData = [
            {
                "Name": "Bitcoin (BTC)",
                "Market Data": {
                "Price": 28000,
                "Market Capitalization": 528000000000,
                "Liquidity": 0.1,
                "24h Volume": 40000000000
                },
                "On-Chain Data": {
                "Transaction Data": 10,
                "Wallet Activity": 10,
                "Address Balances": 0.3
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 9,
                "Social Media Sentiment": 8,
                "Forums": 9,
                "Sentiment Rank": 9
                },
                "Regulatory Data": {
                "Compliance": 7,
                "Legal Status": 8,
                "SEC Verification": 1,
                "Regulatory Risk": 3
                },
                "Blockchain Data": {
                "Active Addresses": 9,
                "Network Hash Rate": 10,
                "Mining Difficulty": 10,
                "Decentralization": 10
                },
                "Smart Contract Code Rating": 0
            },
            {
                "Name": "Ethereum (ETH)",
                "Market Data": {
                "Price": 1800,
                "Market Capitalization": 210000000000,
                "Liquidity": 0.15,
                "24h Volume": 16000000000
                },
                "On-Chain Data": {
                "Transaction Data": 10,
                "Wallet Activity": 10,
                "Address Balances": 0.3
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 8,
                "Social Media Sentiment": 9,
                "Forums": 9,
                "Sentiment Rank": 9
                },
                "Regulatory Data": {
                "Compliance": 8,
                "Legal Status": 9,
                "SEC Verification": 1,
                "Regulatory Risk": 3
                },
                "Blockchain Data": {
                "Active Addresses": 10,
                "Network Hash Rate": 10,
                "Mining Difficulty": 9,
                "Decentralization": 9
                },
                "Smart Contract Code Rating": 10
            },
            {
                "Name": "Tether (USDT)",
                "Market Data": {
                "Price": 1,
                "Market Capitalization": 83000000000,
                "Liquidity": 1,
                "24h Volume": 60000000000
                },
                "On-Chain Data": {
                "Transaction Data": 10,
                "Wallet Activity": 10,
                "Address Balances": 0.1
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 4,
                "Social Media Sentiment": 5,
                "Forums": 6,
                "Sentiment Rank": 5
                },
                "Regulatory Data": {
                "Compliance": 5,
                "Legal Status": 7,
                "SEC Verification": 0,
                "Regulatory Risk": 7
                },
                "Blockchain Data": {
                "Active Addresses": 9,
                "Network Hash Rate": 0,
                "Mining Difficulty": 0,
                "Decentralization": 4
                },
                "Smart Contract Code Rating": 0
            },
            {
                "Name": "Binance Coin (BNB)",
                "Market Data": {
                "Price": 350,
                "Market Capitalization": 58000000000,
                "Liquidity": 0.1,
                "24h Volume": 1500000000
                },
                "On-Chain Data": {
                "Transaction Data": 9,
                "Wallet Activity": 8,
                "Address Balances": 0.2
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 7,
                "Social Media Sentiment": 8,
                "Forums": 7,
                "Sentiment Rank": 8
                },
                "Regulatory Data": {
                "Compliance": 5,
                "Legal Status": 7,
                "SEC Verification": 0,
                "Regulatory Risk": 6
                },
                "Blockchain Data": {
                "Active Addresses": 8,
                "Network Hash Rate": 7,
                "Mining Difficulty": 7,
                "Decentralization": 5
                },
                "Smart Contract Code Rating": 9
            },
            {
                "Name": "Avalanche (AVAX)",
                "Market Data": {
                "Price": 18,
                "Market Capitalization": 7000000000,
                "Liquidity": 0.2,
                "24h Volume": 300000000
                },
                "On-Chain Data": {
                "Transaction Data": 8,
                "Wallet Activity": 7,
                "Address Balances": 0.4
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 7,
                "Social Media Sentiment": 8,
                "Forums": 7,
                "Sentiment Rank": 7
                },
                "Regulatory Data": {
                "Compliance": 7,
                "Legal Status": 8,
                "SEC Verification": 0,
                "Regulatory Risk": 4
                },
                "Blockchain Data": {
                "Active Addresses": 7,
                "Network Hash Rate": 8,
                "Mining Difficulty": 8,
                "Decentralization": 6
                },
                "Smart Contract Code Rating": 8
            },
            {
                "Name": "HEX",
                "Market Data": {
                "Price": 0.05,
                "Market Capitalization": 10000000000,
                "Liquidity": 0.2,
                "24h Volume": 50000000
                },
                "On-Chain Data": {
                "Transaction Data": 6,
                "Wallet Activity": 5,
                "Address Balances": 0.5
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 4,
                "Social Media Sentiment": 5,
                "Forums": 4,
                "Sentiment Rank": 5
                },
                "Regulatory Data": {
                "Compliance": 3,
                "Legal Status": 5,
                "SEC Verification": 0,
                "Regulatory Risk": 8
                },
                "Blockchain Data": {
                "Active Addresses": 6,
                "Network Hash Rate": 6,
                "Mining Difficulty": 6,
                "Decentralization": 5
                },
                "Smart Contract Code Rating": 4
            },
            {
                "Name": "SafeMoon",
                "Market Data": {
                "Price": 0.0000015,
                "Market Capitalization": 5000000000,
                "Liquidity": 0.1,
                "24h Volume": 1000000000
                },
                "On-Chain Data": {
                "Transaction Data": 5,
                "Wallet Activity": 5,
                "Address Balances": 0.4
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 3,
                "Social Media Sentiment": 4,
                "Forums": 5,
                "Sentiment Rank": 4
                },
                "Regulatory Data": {
                "Compliance": 2,
                "Legal Status": 3,
                "SEC Verification": 0,
                "Regulatory Risk": 9
                },
                "Blockchain Data": {
                "Active Addresses": 6,
                "Network Hash Rate": 0,
                "Mining Difficulty": 0,
                "Decentralization": 4
                },
                "Smart Contract Code Rating": 3
            },
            {
                "Name": "Tron (TRX)",
                "Market Data": {
                "Price": 0.1,
                "Market Capitalization": 8000000000,
                "Liquidity": 0.2,
                "24h Volume": 5000000000
                },
                "On-Chain Data": {
                "Transaction Data": 7,
                "Wallet Activity": 6,
                "Address Balances": 0.3
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 4,
                "Social Media Sentiment": 5,
                "Forums": 6,
                "Sentiment Rank": 5
                },
                "Regulatory Data": {
                "Compliance": 5,
                "Legal Status": 6,
                "SEC Verification": 0,
                "Regulatory Risk": 7
                },
                "Blockchain Data": {
                "Active Addresses": 6,
                "Network Hash Rate": 5,
                "Mining Difficulty": 7,
                "Decentralization": 5
                },
                "Smart Contract Code Rating": 4
            },
            {
                "Name": "Verge (XVG)",
                "Market Data": {
                "Price": 0.02,
                "Market Capitalization": 300000000,
                "Liquidity": 0.15,
                "24h Volume": 10000000
                },
                "On-Chain Data": {
                "Transaction Data": 5,
                "Wallet Activity": 5,
                "Address Balances": 0.6
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 4,
                "Social Media Sentiment": 4,
                "Forums": 5,
                "Sentiment Rank": 4
                },
                "Regulatory Data": {
                "Compliance": 3,
                "Legal Status": 4,
                "SEC Verification": 0,
                "Regulatory Risk": 9
                },
                "Blockchain Data": {
                "Active Addresses": 4,
                "Network Hash Rate": 4,
                "Mining Difficulty": 3,
                "Decentralization": 5
                },
                "Smart Contract Code Rating": 3
            },
            {
                "Name": "BitTorrent (BTT)",
                "Market Data": {
                "Price": 0.000002,
                "Market Capitalization": 1000000000,
                "Liquidity": 0.1,
                "24h Volume": 20000000
                },
                "On-Chain Data": {
                "Transaction Data": 6,
                "Wallet Activity": 5,
                "Address Balances": 0.5
                },
                "Whitepapers": 1,
                "Social Sentiment Data": {
                "News": 5,
                "Social Media Sentiment": 5,
                "Forums": 6,
                "Sentiment Rank": 5
                },
                "Regulatory Data": {
                "Compliance": 4,
                "Legal Status": 5,
                "SEC Verification": 0,
                "Regulatory Risk": 8
                },
                "Blockchain Data": {
                "Active Addresses": 6,
                "Network Hash Rate": 0,
                "Mining Difficulty": 0,
                "Decentralization": 4
                },
                "Smart Contract Code Rating": 4
            },
            
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

        print(normalized_weights)

        for i in range(0,len(cryptocurrency_data)):
            c = cryptocurrency_data[i];
            if(c['symbol'].upper() == str(cryptoCurr).upper() or c['name'].lower() == str(cryptoCurr).lower()):
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({
                        "weights": normalized_weights,
                        "cryptoCurrencyMetrics": c,
                        "cryptoData": cryptoData[i]
                    })
                }
        else:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    'message': 'Error Occured'
                })
            }


    return Response(status=200,data={"message": analyze(cryptoCurr)})