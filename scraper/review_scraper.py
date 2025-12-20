import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'Accepted-Language':'en-US,en:q=0.5'
}


def get_product_reviews(search_url):
    page = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")

    product_cards = soup.find_all("div", {"data-component-type": "s-search-result"})
    product_url = None

    for card in product_cards:
        # 🚫 Skip sponsored results
        if card.select_one(".puis-label-popover-default"):
            continue

        link = card.select_one("a.a-link-normal.s-no-outline")
        if link and link.get("href"):
            product_url = "https://www.amazon.in" + link["href"]
            break

    if not product_url:
        raise Exception("No non-sponsored product found")

    print("Product URL:", product_url)

    product_page = requests.get(product_url, headers=HEADERS)
    product_soup = BeautifulSoup(product_page.content, "html.parser")

    review_containers = product_soup.find_all("div", {"data-hook": "review"})
    reviews = []

    reviews = product_soup.find_all("span", {"data-hook": "review-body"}) 
    return [r.get_text(strip=True) for r in reviews]



# search_url = "https://www.amazon.in/s?k=Samsung+Galaxy+Z+Fold7%3A+Raising+the+Bar+for+Smartphones&crid=2W8O6GD1INAA0&sprefix=sa%2Caps%2C220&ref=nb_sb_noss_2"
# reviews = get_product_reviews(search_url)
# print(type(reviews))
# print(len(reviews))
# for r in reviews:
#     print(r)
#     print("-" * 50)