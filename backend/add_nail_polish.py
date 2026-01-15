
import os
import django
import sys

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Product, Category

def add_nail_polish():
    # Ensure Category Exists
    cat, created = Category.objects.get_or_create(name="nail polish", defaults={"slug": "nail-polish"})
    if created:
        print("Created 'nail polish' category.")

    polishes = [
        {"name": "Crimson Red", "slug": "nail-crimson-red", "color": "#DC143C", "desc": "Classic bold red."},
        {"name": "Midnight Blue", "slug": "nail-midnight-blue", "color": "#191970", "desc": "Deep glossy blue."},
        {"name": "Emerald Green", "slug": "nail-emerald-green", "color": "#50C878", "desc": "Rich jewel-toned green."},
        {"name": "Metallic Gold", "slug": "nail-metallic-gold", "color": "#FFD700", "desc": "Shimmering party gold."},
        {"name": "Lavender Haze", "slug": "nail-lavender-haze", "color": "#E6E6FA", "desc": "Soft pastel purple."},
        {"name": "Pitch Black", "slug": "nail-pitch-black", "color": "#000000", "desc": "Edgy glossy black."},
        {"name": "Bubblegum Pink", "slug": "nail-bubblegum-pink", "color": "#FF69B4", "desc": "Fun and bright pink."},
        {"name": "Nude Beige", "slug": "nail-nude-beige", "color": "#F5F5DC", "desc": "Elegant everyday neutral."}
    ]

    print(f"\nAdding {len(polishes)} Nail Polishes...")
    
    for i, p in enumerate(polishes):
        prod, created = Product.objects.get_or_create(
            slug=p['slug'],
            defaults={
                "name": f"Nail Polish - {p['name']}",
                "description": p['desc'],
                "price": 150.00,
                "category": cat,
                "image": "products/nail_polish_default.png",
                "rating": 4.5,
                "stock": 100,
                "is_featured": True,
                "is_trending": i < 4, # Make first 4 trending
                "shades": [p['color']]
            }
        )
        if created:
            print(f" > Added: {p['name']}")
        else:
            print(f" > Skipped (Already exists): {p['name']}")

    print("\nDone! Nail Polishes added to Local Database.")

if __name__ == "__main__":
    add_nail_polish()
