import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Product, Category

print("--- Categories ---")
categories = Category.objects.all()
for c in categories:
    print(f"ID: {c.id}, Name: '{c.name}', Slug: '{c.slug}'")

print("\n--- Products & Categories ---")
products = Product.objects.all()
for p in products:
    cat_name = p.category.name if p.category else "None"
    print(f"ID: {p.id}, Name: '{p.name}', Category: '{cat_name}'")
