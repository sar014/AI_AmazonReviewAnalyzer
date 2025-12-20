import requests
import os
from dotenv import load_dotenv

load_dotenv()

IMGBB_KEY = os.getenv("IMGBB_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


def get_image_url(image_path):
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": IMGBB_KEY}

    with open(image_path, "rb") as img:
        response = requests.post(url, data=payload, files={"image": img})

    return response.json()["data"]["url"]


def reverse_image_search(img_url):
    url = "https://reverse-image-search1.p.rapidapi.com/reverse-image-search"

    params = {
        "url": img_url,
        "limit": "10",
        "safe_search": "blur"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "reverse-image-search1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()["data"][0]["title"]
