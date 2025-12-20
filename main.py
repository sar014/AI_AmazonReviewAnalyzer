from image_search.reverse_image import get_image_url, reverse_image_search
from scraper.amazon_scraper import search_amazon
from scraper.review_scraper import get_product_reviews
import joblib
from llm.text_summarizer import summarize_reviews

model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

image_path = "images/trial2.png"

img_url = get_image_url(image_path)
product_name = reverse_image_search(img_url)

print("Detected product:", product_name)

search_url = search_amazon(product_name)
reviews = get_product_reviews(search_url)

review_data = []

for r in reviews:  # top 5 reviews
    review_vector = vectorizer.transform([r])
    sentiment = model.predict(review_vector)[0]
    review_data.append({"text": r, "sentiment": sentiment})

for rd in review_data:
    print(f"Review: {rd['text']}\nSentiment: {rd['sentiment']}\n{'-'*50}")

# Summarize reviews using LLM
review_texts = [rd["text"] for rd in review_data]
summary = summarize_reviews(review_texts)


print("\nSummary (Pros & Cons):")
print(summary)
