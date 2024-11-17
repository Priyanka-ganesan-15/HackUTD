import json

def calculate_smart_contract_score(contract_quality, audit_reports, developer_activity):
    return round((contract_quality * 0.4 + audit_reports * 0.3 + developer_activity * 0.3), 2)

def process_smartcontract(data_file, output_file):
    with open(data_file, 'r') as f:
        data = json.load(f)

    results = []
    for item in data:
        score = calculate_smart_contract_score(
            item['contract_quality'], item['audit_reports'], item['developer_activity']
        )
        results.append({'name': item['name'], 'smartcontract_score': score})
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

# Example Usage
if __name__ == "__main__":
    process_smartcontract('data/smartcontract_data.json', 'results/smartcontract_score_results.json')
