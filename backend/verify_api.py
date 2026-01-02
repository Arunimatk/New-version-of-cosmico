import requests
import json

try:
    response = requests.get('http://127.0.0.1:8000/api/products/')
    if response.status_code == 200:
        products = response.json()
        print(f"Success! Found {len(products)} products.")
        for p in products:
            print(f"- {p['name']} (Category: {p['category_name']}, Shades: {p['shades']})")
    else:
        print(f"Failed. Status: {response.status_code}")
except Exception as e:
    print(f"Error connecting: {e}")
