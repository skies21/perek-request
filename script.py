import json
import os

import requests
from dotenv import load_dotenv

product_url = "https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/product/plu3604600"
api_url = "https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/product/plu3604600"
load_dotenv()

auth_token = os.getenv("AUTH_TOKEN")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Auth': auth_token,
}

response = requests.get(api_url, headers=headers)
data = response.json().get("content")

product_info = {
    "content_url": product_url,
    "name": data.get("title"),
    "code": data.get("plu"),
    "description": data.get("description"),
    "price_sale": data.get("priceTag", {}).get("price") / 100,
    "price": data.get("priceTag", {}).get("grossPrice") / 100,
    "rating": data.get("rating"),
    "comment_count": data.get("reviewCount"),
    "brand": data.get("analyticsInfo", {})[1].get("value"),
    "categories": [
        data.get("primaryCategory", {}).get("title"),
        data.get("catalogPrimaryCategory", {}).get("title")
    ],
    "images": [{"image_url": img.get("cropUrlTemplate")} for img in data.get("images", []) if img.get("cropUrlTemplate")]
}

with open("product_info.json", "w", encoding="utf-8") as f:
    json.dump(product_info, f, ensure_ascii=False, indent=4)
