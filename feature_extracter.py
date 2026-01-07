import http.client
import json
from urllib.parse import urlparse


def extract_asin(product_url: str) -> str:
    """
    Extract ASIN from an Amazon product URL
    """
    parsed = urlparse(product_url)
    path_parts = parsed.path.split("/")

    if "dp" in path_parts:
        return path_parts[path_parts.index("dp") + 1]
    elif "gp" in path_parts:
        return path_parts[path_parts.index("product") + 1]
    else:
        raise ValueError("ASIN not found in URL")


def get_review_comments(product_url: str, country="IN"):
    """
    Fetch review comments for a given Amazon product URL
    """
    asin = extract_asin(product_url)

    conn = http.client.HTTPSConnection("real-time-amazon-data.p.rapidapi.com")

    headers = {
        "x-rapidapi-key": "4334a8845dmsh546f794be99d5ebp1905b0jsn23a2c7988b17",
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
    }

    endpoint = f"/top-product-reviews?asin={asin}&country={country}"
    conn.request("GET", endpoint, headers=headers)

    res = conn.getresponse()
    data = res.read()

    response_json = json.loads(data.decode("utf-8"))
    reviews = response_json["data"]["reviews"]

    
    structured_reviews = []

    for r in reviews:
        if r["review_comment"]:
            structured_reviews.append({
                "id": r["review_id"],
                "title": r["review_title"],
                "text": r["review_comment"]
            })

    return structured_reviews
