import http.client
import json
from urllib.parse import quote


def get_product_url(product_name: str, country="IN") -> str | None:
    """
    Search product on Amazon via RapidAPI and return product URL
    """

    query = quote(product_name)
    print(f"Query: {query}")

    conn = http.client.HTTPSConnection("real-time-amazon-data.p.rapidapi.com")

    headers = {
        "x-rapidapi-key": "4334a8845dmsh546f794be99d5ebp1905b0jsn23a2c7988b17",
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
    }

    endpoint = (
        f"/search?query={query}&page=1&country={country}"
        f"&sort_by=RELEVANCE&product_condition=ALL"
        f"&is_prime=false&deals_and_discounts=NONE"
    )

    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()

    response_json = json.loads(data.decode("utf-8"))

    products = response_json.get("data", {}).get("products", [])

    if not products:
        return None

    asin = products[0].get("asin")
    if not asin:
        return None

    return f"https://www.amazon.in/dp/{asin}"
