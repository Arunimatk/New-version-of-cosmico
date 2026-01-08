import requests
import json
import sys

# Fetch data from live API
print("Fetching data from Live API...")
try:
    response = requests.get('https://cosmico-backend-arun.onrender.com/api/products/')
    response.raise_for_status()
    products = response.json()
except Exception as e:
    print(f"Error fetching data: {e}")
    sys.exit(1)

fixture = []

# Map API response to Django Fixture format
for product in products:
    item = {
        "model": "api.product",
        "pk": product['id'],
        "fields": {
            "name": product['name'],
            "slug": product['slug'],
            "description": product['description'],
            "price": product['price'],
            "category": product['category'], 
            "image": product['image'], # This should be the Cloudinary URL
            "rating": product.get('rating', 0),
            "stock": product.get('stock', 0),
            "is_featured": product.get('is_featured', False),
            "is_trending": product.get('is_trending', False),
            "created_at": product.get('created_at'),
            "shades": product.get('shades', [])
        }
    }
    fixture.append(item)

# Load existing dummy users/categories from data.json to preserve them
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
        # Filter out old products to avoid duplicates/conflicts, keep other models
        others = [item for item in existing_data if item['model'] != 'api.product']
        final_data = others + fixture
except FileNotFoundError:
    final_data = fixture

# Save to data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=2)

print(f"Successfully rescued {len(fixture)} products and saved to data.json")
