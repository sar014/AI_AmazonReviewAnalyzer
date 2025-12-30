from image_search.reverse_image import get_image_url, reverse_image_search
from scraper.amazon_scraper import search_amazon
from scraper.review_scraper import get_product_reviews,generate_product_url
from scraper.feature_scrapper import get_product_features

import joblib
from llm.text_summarizer import summarize_reviews
from llm.feature_summarizer import summarize_features

model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

image_path = "images/trial2.png"

img_url = get_image_url(image_path)
product_name = reverse_image_search(img_url)

print("Detected product:", product_name)

search_url = search_amazon(product_name)
product_url = generate_product_url(search_url)

print(product_url)

reviews = get_product_reviews(product_url)
features = get_product_features(product_url)
feature_summary = summarize_features(features)
print(feature_summary)

# for f in features:
#     feature_summary = summarize_features(f)
#     print("=" * 50)
#     print(feature_summary)
#     print("=" * 50)

review_data = []

for r in reviews:  
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
