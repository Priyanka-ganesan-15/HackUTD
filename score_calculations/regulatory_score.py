import json

def calculate_regulatory_score(is_sec_verified, country_regulations):
    return round((is_sec_verified * 0.7 + country_regulations * 0.3) * 10, 2)

def process_regulatory(data_file, output_file):
    with open(data_file, 'r') as f:
        data = json.load(f)

    results = []
    for item in data:
        score = calculate_regulatory_score(item['is_sec_verified'], item['country_regulations'])
        results.append({'name': item['name'], 'regulatory_score': score})
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

# Example Usage
if __name__ == "__main__":
    process_regulatory('data/regulatory_data.json', 'results/regulatory_score_results.json')
