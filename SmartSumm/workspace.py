def generate_summary(reviews): #Adding more context
    restaurant_name = reviews[0]['Restaurant']  # Assuming all reviews are for the same restaurant
    all_reviews_text = "\n".join([review['Review'] for review in reviews])
    prompt = f"Summarize the reviews for {restaurant_name}. The reviews mention:\n{all_reviews_text}"
    try:
        output = lm.do(prompt)
        return output.strip()
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None

###
def generate_summary(reviews):
    positive_reviews = [review['Review'] for review in reviews if review['Sentiment'] == 'Positive']
    negative_reviews = [review['Review'] for review in reviews if review['Sentiment'] == 'Negative']

    positive_text = "\n".join(positive_reviews)
    negative_text = "\n".join(negative_reviews)

    prompt = f"Summarize the positive and negative sentiments for this restaurant:\nPositive reviews:\n{positive_text}\nNegative reviews:\n{negative_text}"

    try:
        output = lm.do(prompt)
        return output.strip()
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None
