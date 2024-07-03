import csv
import sys
import languagemodels as lm


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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a restaurant name as an argument.")
        sys.exit(1)

    restaurant_name = sys.argv[1]
    reviews_file = 'restaurant-reviews.csv'

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
        # print(output)
        summary = output
        print(f"\nSummary of reviews for '{restaurant_name}':\n")
        print(summary)
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
