import requests
from bs4 import BeautifulSoup

# User Agent : simulate a real browser
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'Accepted-Language':'en-US,en:q=0.5'
}


def generate_product_url(search_url):
    page = requests.get(search_url, headers=HEADERS) # Sends request to Amazon
    soup = BeautifulSoup(page.content, "html.parser") # Parse HTML, allows easy navigation and searching of elements

    product_cards = soup.find_all("div", {"data-component-type": "s-search-result"}) # Find all div of typedata-component-type="s-search-result"
    product_url = None

    for card in product_cards:
        # Skip sponsored results
        if card.select_one(".puis-label-popover-default"):
            continue
        
        # Extract product URL
        link = card.select_one("a.a-link-normal.a-text-normal") or card.select_one("a[href^='/dp/']")
        if link and link.get("href"):
            product_url = "https://www.amazon.in" + link["href"]
            break
    return product_url

def get_product_reviews(product_url):
    if not product_url:
        raise Exception("No non-sponsored product found")

    product_page = requests.get(product_url, headers=HEADERS)
    product_soup = BeautifulSoup(product_page.content, "html.parser")

    review_containers = product_soup.find_all(attrs={"data-hook": "review"})
    print("\nReview Containers:", review_containers)
    reviews = []

    with open("debug.txt", "w", encoding="utf-8") as f:
        f.write(product_page.text)

    for div in review_containers:
        body_span = div.find("span", {"data-hook": "review-body"})
        if not body_span:
            continue
        # text is usually in inner span
        text_span = body_span.find("span") or body_span
        review_text = text_span.get_text(strip=True)
        if review_text:
            reviews.append(review_text)

    return reviews


