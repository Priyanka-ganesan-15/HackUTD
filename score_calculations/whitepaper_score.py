import json

def calculate_whitepaper_exists(whitepaper_link):
    return 1 if whitepaper_link else 0

def process_whitepaper(data_file, output_file):
    with open(data_file, 'r') as f:
        data = json.load(f)

    results = []
    for item in data:
        score = calculate_whitepaper_exists(item['whitepaper_link'])
        results.append({'name': item['name'], 'whitepaper_exists': score})
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

# Example Usage
if __name__ == "__main__":
    process_whitepaper('data/whitepaper_data.json', 'results/whitepaper_results.json')
