from textblob import TextBlob
import json

def calculate_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity * 10  # Scale to 0-10
    return round(sentiment_score, 2)

def process_sentiment(data_file, output_file):
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    results = []
    for item in data:
        text = item['text']
        score = calculate_sentiment(text)
        results.append({'name': item['name'], 'sentiment_score': score})
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

# Example Usage
if __name__ == "__main__":
    process_sentiment('data/sentiment_data.json', 'results/sentiment_score_results.json')
