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

    #  About this item (Feature bullets)
    feature_section = soup.find("div", id="feature-bullets")

    if feature_section:
        items = feature_section.find_all("span", class_="a-list-item")
        for item in items:
            text = item.get_text(strip=True)
            if text:
                features.append(text)

    return features

