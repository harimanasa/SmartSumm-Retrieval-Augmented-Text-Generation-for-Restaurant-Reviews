import csv
import sys
import languagemodels as lm


# Function to read restaurant reviews from CSV
def read_reviews_csv(file_path):
    reviews = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviews.append(row)
    return reviews


# Function to read evaluation set CSV
def read_evaluation_set(file_path):
    evaluation_set = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            evaluation_set.append(row)
    return evaluation_set


# Function to filter reviews for a specific restaurant name
def get_reviews_for_restaurant(reviews, restaurant_name):
    filtered_reviews = []
    for review in reviews:
        if review['Restaurant'] == restaurant_name:
            filtered_reviews.append(review)
    return filtered_reviews


# Function to generate summary using LLM
def generate_summary(reviews):
    # Prepare review text for processing by Language Model
    all_reviews_text = "\n".join([review['Review'] for review in reviews])

    # Construct prompt for LLM
    prompt = f"{all_reviews_text}"

    # Use the Language Model to generate a summary
    try:
        output = lm.do(prompt)
        return output.strip()  # Remove leading/trailing whitespaces
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None


# Function to update evaluation set with generated summaries
def update_evaluation_set(evaluation_set, restaurant_name, generated_summary):
    for entry in evaluation_set:
        if entry['resturant_name'] == restaurant_name:
            entry['llm_generated_response'] = generated_summary


# Function to write updated evaluation set back to CSV
def write_evaluation_set(file_path, evaluation_set):
    fieldnames = evaluation_set[0].keys()

    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(evaluation_set)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a restaurant name as an argument.")
        sys.exit(1)

    restaurant_name = sys.argv[1]
    reviews_file = 'restaurant-reviews.csv'
    evaluation_file = 'resturant-evaluation-set.csv'

    # Read restaurant reviews from CSV
    reviews = read_reviews_csv(reviews_file)

    # Read evaluation set from CSV
    evaluation_set = read_evaluation_set(evaluation_file)

    # Filter reviews for the specified restaurant
    restaurant_reviews = get_reviews_for_restaurant(reviews, restaurant_name)

    if not restaurant_reviews:
        print(f"No reviews found for restaurant '{restaurant_name}'.")
        sys.exit(0)

    # Generate summary using LLM
    generated_summary = generate_summary(restaurant_reviews)

    if generated_summary:
        # Update evaluation set with generated summary
        update_evaluation_set(evaluation_set, restaurant_name, generated_summary)

        # Write updated evaluation set back to CSV
        write_evaluation_set(evaluation_file, evaluation_set)

        print(f"\nSummary generated and updated for restaurant '{restaurant_name}' in '{evaluation_file}'.")
    else:
        print(f"\nFailed to generate summary for restaurant '{restaurant_name}'.")

