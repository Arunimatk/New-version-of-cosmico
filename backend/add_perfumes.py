
import os
import django
import sys

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Product, Category

def add_perfumes():
    # Ensure Category Exists
    cat, created = Category.objects.get_or_create(name="perfume", defaults={"slug": "perfume"})
    if created:
        print("Created 'perfume' category.")

    perfumes = [
        {
            "name": "Midnight Rose",
            "slug": "midnight-rose",
            "description": "A dark, romantic floral scent with notes of rose and amber. Perfect for evening wear.",
            "price": 1200.00,
            "image": "products/perfume_default.png",
            "rating": 4.8,
            "stock": 50
        },
        {
            "name": "Ocean Breeze",
            "slug": "ocean-breeze",
            "description": "Fresh and aquatic, capturing the essence of the sea. ideal for daily use.",
            "price": 950.00,
            "image": "products/perfume_default.png",
            "rating": 4.5,
            "stock": 50
        },
        {
            "name": "Vanilla Dreams",
            "slug": "vanilla-dreams",
            "description": "Sweet and comforting vanilla with a hint of musk. A warm, inviting fragrance.",
            "price": 1100.00,
            "image": "products/perfume_default.png",
            "rating": 4.7,
            "stock": 50
        },
        {
            "name": "Citrus Zest",
            "slug": "citrus-zest",
            "description": "A burst of lemon and orange energy. energizing and bright.",
            "price": 850.00,
            "image": "products/perfume_default.png",
            "rating": 4.6,
            "stock": 50
        },
        {
            "name": "Golden Amber",
            "slug": "golden-amber",
            "description": "Rich and warm with deep resinous notes. A scent of pure luxury.",
            "price": 1350.00,
            "image": "products/perfume_default.png",
            "rating": 4.9,
            "stock": 30
        },
        {
            "name": "Mystic Oud",
            "slug": "mystic-oud",
            "description": "Exotic and intense oud wood fragrance for a mysterious aura.",
            "price": 1500.00,
            "image": "products/perfume_default.png",
            "rating": 5.0,
            "stock": 25
        },
        {
            "name": "Spring Blossom",
            "slug": "spring-blossom",
            "description": "Light and airy floral bouquet, like a walk in a garden.",
            "price": 900.00,
            "image": "products/perfume_default.png",
            "rating": 4.4,
            "stock": 60
        },
        {
            "name": "Spicy Noir",
            "slug": "spicy-noir",
            "description": "Bold spices mixed with dark chocolate notes. For the daring.",
            "price": 1150.00,
            "image": "products/perfume_default.png",
            "rating": 4.7,
            "stock": 40
        }
    ]

    print(f"\nAdding {len(perfumes)} perfumes...")
    
    for p in perfumes:
        prod, created = Product.objects.get_or_create(
            slug=p['slug'],
            defaults={
                "name": p['name'],
                "description": p['description'],
                "price": p['price'],
                "category": cat,
                "image": p['image'],
                "rating": p['rating'],
                "stock": p['stock'],
                "is_featured": True,
                "is_trending": True,
                "shades": ["Standard"]
            }
        )
        if created:
            print(f" > Added: {p['name']}")
        else:
            print(f" > Skipped (Already exists): {p['name']}")

    print("\nDone! Perfumes added to Local Database.")

if __name__ == "__main__":
    add_perfumes()
