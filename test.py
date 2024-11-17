# test_fetching.py

from data_fetching import get_supported_coins

def test_get_supported_coins():
    coins = get_supported_coins()
    if coins:
        print(f"Successfully fetched {len(coins)} coins.")
        # Optionally, print first 5 coins for verification
        for coin in coins[:5]:
            print(f"Name: {coin['name']}, Symbol: {coin['symbol'].upper()}, ID: {coin['id']}")
    else:
        print("Failed to fetch coins.")

if __name__ == "__main__":
    test_get_supported_coins()
