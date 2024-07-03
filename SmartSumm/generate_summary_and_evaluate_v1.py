import csv
import sys
import languagemodels as lm
from sklearn.metrics import f1_score
from sentence_transformers import SentenceTransformer, util


def read_reviews_csv(file_path):
    reviews = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviews.append(row)
    return reviews


def get_reviews_for_restaurant(reviews, restaurant_name):
    filtered_reviews = []
    for review in reviews:
        if review['Restaurant'] == restaurant_name:
            filtered_reviews.append(review)
    return filtered_reviews


def evaluate_summary(expected_summary, generated_summary):
    # Calculate F1 score
    f1 = f1_score(expected_summary.lower(), generated_summary.lower(), average='weighted')

    # Calculate BERT similarity
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    embeddings1 = model.encode([expected_summary])
    embeddings2 = model.encode([generated_summary])
    bert_similarity = util.pytorch_cos_sim(embeddings1, embeddings2).item()

    return f1, bert_similarity


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a restaurant name as an argument.")
        sys.exit(1)

    restaurant_name = sys.argv[1]
    reviews_file = 'data/resturant-reviews.csv'
    evaluation_file = 'data/resturant-evaluation-set.csv'

    reviews = read_reviews_csv(reviews_file)
    restaurant_reviews = get_reviews_for_restaurant(reviews, restaurant_name)

    if not restaurant_reviews:
        print(f"No reviews found for restaurant '{restaurant_name}'.")
        sys.exit(0)

    # Prepare review text for processing by Language Model
    all_reviews_text = "\n".join([review['Review'] for review in restaurant_reviews])

    # Construct the prompt for the Language Model
    prompt = f"""{all_reviews_text}"""

    # Use the Language Model to generate a summary
    try:
        output = lm.do(prompt)
        summary = output.strip()
        print(f"\nSummary of reviews for '{restaurant_name}':\n")
        print(summary)

        # Update resturant-evaluation-set.csv with llm_generated_response
        with open(evaluation_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows:
            if row['resturant_name'] == restaurant_name:
                row['llm_generated_response'] = summary

        with open(evaluation_file, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = ['resturant_name', 'expected_response', 'llm_generated_response']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)



    #
    #
    #     # Evaluate the generated summary against expected_response
    #     expected_summary = next((row['expected_response'] for row in rows if row['resturant_name'] == restaurant_name), None)
    #     f1_score, bert_similarity = evaluate_summary(expected_summary, summary)
    #     print(f"\nEvaluation Metrics for '{restaurant_name}':")
    #     print(f"F1 Score: {f1_score}")
    #     print(f"BERT Similarity: {bert_similarity}")
    #
    # except Exception as e:
    #     print(f"Error generating summary: {str(e)}")
