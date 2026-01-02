import urllib.request
import json

try:
    print("Attempting to fetch products from http://127.0.0.1:8000/api/products/ ...")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/products/") as response:
        if response.status == 200:
            data = json.loads(response.read().decode())
            print(f"Success! Found {len(data)} products.")
            print("-" * 30)
            for p in data:
                print(f"ID: {p['id']}")
                print(f"Name: {p['name']}")
                print(f"Category Name: {p.get('category_name', 'N/A')}")
                print(f"Image: {p['image']}")
                print("-" * 30)
        else:
            print(f"Failed. Status: {response.status}")
except Exception as e:
    print(f"Error connecting to API: {e}")
