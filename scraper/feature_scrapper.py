import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'Accepted-Language':'en-US,en:q=0.5'
}

def get_product_features(product_url):
    if not product_url:
        raise Exception("Invalid product URL")

    page = requests.get(product_url, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")

    features = []

    # ✅ About this item (Feature bullets)
    feature_section = soup.find("div", id="feature-bullets")

    if feature_section:
        items = feature_section.find_all("span", class_="a-list-item")
        for item in items:
            text = item.get_text(strip=True)
            if text:
                features.append(text)

    return features

# product_url = "https://www.amazon.in/Sony-PlayStation%C2%AE5-Digital-Edition-slim/dp/B0CY5QW186/ref=sr_1_1?dib=eyJ2IjoiMSJ9.W_aORAobBCT42F1MQVtl9n-7-_gBvYVRskt9hxGq29-8xXOwpYGNXWNzvw8fPwBlY6PGDPCdP_ggP9K5Bv-G_8d2LJH5n-_yfhsmXsjB7PlK1Hgt9sy58NoOpPiJGkKxnK4aOFF-KoaEc_Ag2fmgRh-nXCSZ378xpUp_KzaJ7EllRBqwjXAw-DhPqaZ_k64PzfEGiJ7U9PsMKWtXWt2RK4eDkC0ZpCH8_BEUS6oqTvE.SkJcGdMLgecZTmJTNB4BJO4mPX5_l4WUfPdIugXgVkk&dib_tag=se&keywords=Sony+PlayStation%C2%AE5+Digital+Edition+%28slim%29+-+eBay&qid=1766254226&sr=8-1"
# feature_summary = get_product_features(product_url)

# for f in feature_summary:
#     print("="*50)
#     print(f)