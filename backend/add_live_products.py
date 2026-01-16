import os
import django
import sys

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Product, Category

def add_live_products():
    print("Starting product addition...")

    # --- Categories ---
    cat_perfume, _ = Category.objects.get_or_create(name="perfume", defaults={"slug": "perfume"})
    cat_nail, _ = Category.objects.get_or_create(name="nail polish", defaults={"slug": "nail-polish"})

    # --- Perfumes (8 items) ---
    perfumes = [
        {"name": "Elysian Essence", "desc": "A divine blend of jasmine and sandalwood.", "price": 1250, "slug": "elysian-essence"},
        {"name": "Velvet Night", "desc": "Dark orchid and spices for the evening.", "price": 1400, "slug": "velvet-night"},
        {"name": "Azure Sky", "desc": "Fresh ozone and citrus, like a clear sky.", "price": 950, "slug": "azure-sky"},
        {"name": "Golden Hour", "desc": "Warm amber and vanilla, capturing the sunset.", "price": 1100, "slug": "golden-hour"},
        {"name": "Rose Quartz", "desc": "Soft rose offering a delicate floral touch.", "price": 1050, "slug": "rose-quartz"},
        {"name": "Mystic Woods", "desc": "Cedarwood and moss for an earthy grounding.", "price": 1300, "slug": "mystic-woods"},
        {"name": "Citrus Splash", "desc": "Invigorating lemon and bergamot.", "price": 850, "slug": "citrus-splash"},
        {"name": "Opulent Oud", "desc": "Luxurious oud wood and leather.", "price": 1600, "slug": "opulent-oud"},
    ]

    # --- Nail Polishes (8 items) ---
    nail_polishes = [
        {"name": "Ruby Slippers", "desc": "Glittering deep red.", "color": "#E0115F", "slug": "nail-ruby-slippers"},
        {"name": "Sapphire star", "desc": "Metallic heavy blue.", "color": "#0F52BA", "slug": "nail-sapphire-star"},
        {"name": "Emerald City", "desc": "Shimmering green.", "color": "#50C878", "slug": "nail-emerald-city"},
        {"name": "Gold Rush", "desc": "Liquid gold finish.", "color": "#FFD700", "slug": "nail-gold-rush"},
        {"name": "Silver Lining", "desc": "Chrome silver mirror effect.", "color": "#C0C0C0", "slug": "nail-silver-lining"},
        {"name": "Amethyst Aura", "desc": "Holographic purple.", "color": "#9966CC", "slug": "nail-amethyst-aura"},
        {"name": "Obsidian", "desc": "Pure glossy black.", "color": "#000000", "slug": "nail-obsidian"},
        {"name": "Pearl White", "desc": "Iridescent white sheen.", "color": "#F0F8FF", "slug": "nail-pearl-white"},
    ]

    # --- Add Perfumes ---
    for i, p in enumerate(perfumes):
        prod, created = Product.objects.get_or_create(
            slug=p['slug'],
            defaults={
                "name": p['name'],
                "description": p['desc'],
                "price": p['price'],
                "category": cat_perfume,
                "image": "products/perfume_default.png",
                "rating": 4.8,
                "stock": 50,
                "is_featured": True,
                "is_trending": i < 4, # First 4 are trending
                "shades": ["Standard"]
            }
        )
        status = "Added" if created else "Exists"
        print(f"Perfume {status}: {p['name']}")

    # --- Add Nail Polishes ---
    for i, p in enumerate(nail_polishes):
        prod, created = Product.objects.get_or_create(
            slug=p['slug'],
            defaults={
                "name": f"Nail Polish - {p['name']}",
                "description": p['desc'],
                "price": 199.00,
                "category": cat_nail,
                "image": "products/nail_polish_default.png",
                "rating": 4.6,
                "stock": 100,
                "is_featured": True,
                "is_trending": i < 4,
                "shades": [p['color']]
            }
        )
        status = "Added" if created else "Exists"
        print(f"Nail Polish {status}: {p['name']}")

    print("\nDone. Run this script in your Render environment if using a remote DB, or ensure your local DB is connected to the live app.")

if __name__ == "__main__":
    add_live_products()
