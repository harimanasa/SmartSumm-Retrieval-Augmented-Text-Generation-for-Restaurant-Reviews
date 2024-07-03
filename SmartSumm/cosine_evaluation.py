import csv
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

def compute_cosine_similarity(expected_responses, generated_responses):
    # Calculate Cosine Similarity
    vectorizer = TfidfVectorizer()
    tfidf_expected = vectorizer.fit_transform(expected_responses)
    tfidf_generated = vectorizer.transform(generated_responses)
    cosine_similarities = cosine_similarity(tfidf_generated, tfidf_expected)
    return cosine_similarities.mean()

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

    # Extract expected and generated responses
    expected_responses = restaurant_reviews['expected_response'].tolist()
    generated_responses = restaurant_reviews['llm_generated_response'].tolist()

    # Compute BERTScore
    bert_scores = compute_bert_score(expected_responses, generated_responses)

    # Compute Cosine Similarity
    cosine_similarity_score = compute_cosine_similarity(expected_responses, generated_responses)

    # Print evaluation metrics
    print(f"\nEvaluation Metrics for '{restaurant_name}':")
    print(f"BERT Precision: {bert_scores['bert_precision']:.4f}")
    print(f"BERT Recall: {bert_scores['bert_recall']:.4f}")
    print(f"BERT F1: {bert_scores['bert_f1']:.4f}")
    print(f"Cosine Similarity: {cosine_similarity_score:.4f}")
