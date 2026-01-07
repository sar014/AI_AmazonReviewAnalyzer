import streamlit as st
import joblib
from PIL import Image
import tempfile
import os

from image_search.reverse_image import get_image_url, reverse_image_search
from llm.text_summarizer import summarize_reviews
from product_url_extract import get_product_url
from feature_extracter import get_review_comments

st.set_page_config(
    page_title="Image-Based Product Review Analyzer",
    layout="wide"
)

st.title("🖼️ → 🛍️ Product Review Analyzer")
st.write(
    "Upload a product image to extract Amazon reviews, "
    "analyze sentiment, and generate pros & cons."
)

@st.cache_resource
def load_models():
    model = joblib.load("models/sentiment_model.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_models()

uploaded_image = st.file_uploader(
    "Upload product image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", width = 300)

    if st.button("Analyze Product"):
        with st.spinner("Uploading image & detecting product..."):

            # Save image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                image.save(tmp.name)
                image_path = tmp.name

            img_url = get_image_url(image_path)
            product_name = reverse_image_search(img_url)

        st.success(f"Detected product: **{product_name}**")

        with st.spinner("Searching Amazon..."):
            product_url = get_product_url(product_name)
            print("\nProduct URL:", product_url)

        with st.spinner("Extracting reviews..."):
            reviews = get_review_comments(product_url)

        if not reviews:
            st.error("No reviews found.")
            st.stop()
       
        st.subheader("🔗 Product Link")
        st.markdown(f"[Click here to view the product]({product_url})", unsafe_allow_html=True)

        st.subheader("📝 Reviews & Sentiment")

       
        review_data = []

        for r in reviews[:5]:
            review_vector = vectorizer.transform([r["text"]])
            sentiment = model.predict(review_vector)[0]

            review_data.append({
                "text": r["text"],
                "sentiment": sentiment
            })

            emoji = "😊" if sentiment == "positive" else "😡" if sentiment == "negative" else "😐"

            st.markdown(f"""
            **{emoji} {sentiment.capitalize()} Review**  
            **🆔 Review ID:** `{r["id"]}`  
            **📝 Title:** *{r["title"]}*  

            > {r["text"]}
            """)

        with st.spinner("Generating pros & cons..."):
            review_texts = [r["text"] for r in reviews]
            summary = summarize_reviews(review_texts)

        st.subheader("📌 Pros & Cons (LLM Generated)")
        st.markdown(summary)

        os.remove(image_path)
