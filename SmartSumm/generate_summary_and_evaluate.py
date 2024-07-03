import csv
import sys
from rouge_score import rouge_scorer

import languagemodels as lm

# Function to read reviews from CSV file
def read_reviews_csv(file_path):
    reviews = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviews.append(row)
    return reviews

# Function to filter reviews for a specific restaurant
def get_reviews_for_restaurant(reviews, restaurant_name):
    filtered_reviews = []
    for review in reviews:
        if review['Restaurant'] == restaurant_name:
            filtered_reviews.append(review)
    return filtered_reviews

# Function to generate summary using LLM
def generate_summary(reviews):
    all_reviews_text = "\n".join([review['Review'] for review in reviews])
    prompt = f"""{all_reviews_text}"""

    try:
        output = lm.do(prompt)
        return output.strip()
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None

# Function to evaluate ROUGE scores
def evaluate_rouge_scores(expected_response, llm_generated_response):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(expected_response, llm_generated_response)
    return scores

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a restaurant name as an argument.")
        sys.exit(1)

    restaurant_name = sys.argv[1]
    reviews_file = 'data/resturant-reviews.csv'
    evaluation_file = 'data/resturant-evaluation-set.csv'

    # Read restaurant reviews
    reviews = read_reviews_csv(reviews_file)
    restaurant_reviews = get_reviews_for_restaurant(reviews, restaurant_name)

    if not restaurant_reviews:
        print(f"No reviews found for restaurant '{restaurant_name}'.")
        sys.exit(0)

    # Generate summary using LLM
    llm_generated_response = generate_summary(restaurant_reviews)

    if not llm_generated_response:
        sys.exit(1)

    # Evaluate ROUGE scores
    with open(evaluation_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['resturant_name'] == restaurant_name:
                expected_response = row['expected_response']
                rouge_scores = evaluate_rouge_scores(expected_response, llm_generated_response)
                print(f"\nROUGE Scores for '{restaurant_name}':\n")
                print(rouge_scores)
                break
