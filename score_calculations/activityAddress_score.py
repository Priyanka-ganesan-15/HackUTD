import json

def calculate_active_address_score(daily_active_addresses, transaction_volume):
    max_addresses = 1_000_000
    max_volume = 1_000_000_000
    address_score = (daily_active_addresses / max_addresses) * 5
    volume_score = (transaction_volume / max_volume) * 5
    return round(address_score + volume_score, 2)

def process_active_address(data_file, output_file):
    with open(data_file, 'r') as f:
        data = json.load(f)

    results = []
    for item in data:
        score = calculate_active_address_score(item['daily_active_addresses'], item['transaction_volume'])
        results.append({'name': item['name'], 'active_address_score': score})
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

# Example Usage
if __name__ == "__main__":
    process_active_address('data/active_address_data.json', 'results/active_address_score_results.json')
