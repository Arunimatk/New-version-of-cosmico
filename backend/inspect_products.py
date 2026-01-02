import os
import django
import sys
import json

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Product

print("--- Product Inspection ---")
products = Product.objects.all()
for p in products:
    print(f"ID: {p.id}")
    print(f"Name: {p.name}")
    print(f"Image Field: {p.image}")
    try:
        print(f"Image URL: {p.image.url}")
    except ValueError:
        print("Image URL: No file associated")
    
    print(f"Shades (Raw): {p.shades}")
    print(f"Shades Type: {type(p.shades)}")
    print(f"Price: {p.price}")
    print("-" * 20)
