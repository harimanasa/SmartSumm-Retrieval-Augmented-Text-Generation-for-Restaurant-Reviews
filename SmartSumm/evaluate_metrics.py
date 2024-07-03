import csv
import sys
import pandas as pd
from bert_score import score

def read_reviews_csv(file_path):
    reviews = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviews.append(row)
    return reviews

def compute_bert_score(expected_responses, generated_responses):
    # Calculate BERTScore
    P, R, F1 = score(generated_responses, expected_responses, lang='en', verbose=False)
    return {
        'bert_precision': P.mean().item(),
        'bert_recall': R.mean().item(),
        'bert_f1': F1.mean().item()
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a restaurant name as an argument.")
        sys.exit(1)

    restaurant_name = sys.argv[1]
    reviews_file = 'data/resturant-evaluation-set.csv'

    # Read CSV into DataFrame
    df = pd.read_csv(reviews_file)

    # Filter reviews for the specified restaurant
    restaurant_reviews = df[df['resturant_name'] == restaurant_name]

    if restaurant_reviews.empty:
        print(f"No reviews found for restaurant '{restaurant_name}' in the CSV.")
        sys.exit(0)

    # Compute BERTScore
    bert_scores = compute_bert_score(restaurant_reviews['expected_response'].tolist(),
                                     restaurant_reviews['llm_generated_response'].tolist())

    print(f"\nBERTScore for '{restaurant_name}':")
    print(f"BERT Precision: {bert_scores['bert_precision']:.4f}")
    print(f"BERT Recall: {bert_scores['bert_recall']:.4f}")
    print(f"BERT F1: {bert_scores['bert_f1']:.4f}")
