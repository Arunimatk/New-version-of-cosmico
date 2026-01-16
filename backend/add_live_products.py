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

    # --- Perfumes (8 items) with Real Images ---
    perfumes = [
        {"name": "Elysian Essence", "desc": "A divine blend of jasmine and sandalwood.", "price": 1250, "slug": "elysian-essence", "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?q=80&w=800&auto=format&fit=crop"},
        {"name": "Velvet Night", "desc": "Dark orchid and spices for the evening.", "price": 1400, "slug": "velvet-night", "image": "https://images.unsplash.com/photo-1594035910387-fea477942698?q=80&w=800&auto=format&fit=crop"},
        {"name": "Azure Sky", "desc": "Fresh ozone and citrus, like a clear sky.", "price": 950, "slug": "azure-sky", "image": "https://images.unsplash.com/photo-1523293188086-b431e90979ec?q=80&w=800&auto=format&fit=crop"},
        {"name": "Golden Hour", "desc": "Warm amber and vanilla, capturing the sunset.", "price": 1100, "slug": "golden-hour", "image": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?q=80&w=800&auto=format&fit=crop"},
        {"name": "Rose Quartz", "desc": "Soft rose offering a delicate floral touch.", "price": 1050, "slug": "rose-quartz", "image": "https://images.unsplash.com/photo-1583467875263-d50dec37a885?q=80&w=800&auto=format&fit=crop"},
        {"name": "Mystic Woods", "desc": "Cedarwood and moss for an earthy grounding.", "price": 1300, "slug": "mystic-woods", "image": "https://images.unsplash.com/photo-1512777576255-a8052001fd6f?q=80&w=800&auto=format&fit=crop"},
        {"name": "Citrus Splash", "desc": "Invigorating lemon and bergamot.", "price": 850, "slug": "citrus-splash", "image": "https://images.unsplash.com/photo-1616084083324-7128795da3c2?q=80&w=800&auto=format&fit=crop"},
        {"name": "Opulent Oud", "desc": "Luxurious oud wood and leather.", "price": 1600, "slug": "opulent-oud", "image": "https://images.unsplash.com/photo-1622618991746-327f993d4f0d?q=80&w=800&auto=format&fit=crop"},
    ]

    # --- Nail Polishes (8 items) with Real Images ---
    nail_polishes = [
        {"name": "Ruby Slippers", "desc": "Glittering deep red.", "color": "#E0115F", "slug": "nail-ruby-slippers", "image": "https://images.unsplash.com/photo-1632516421654-7299557b6408?q=80&w=800&auto=format&fit=crop"},
        {"name": "Sapphire star", "desc": "Metallic heavy blue.", "color": "#0F52BA", "slug": "nail-sapphire-star", "image": "https://images.unsplash.com/photo-1604654894610-df63bc536371?q=80&w=800&auto=format&fit=crop"},
        {"name": "Emerald City", "desc": "Shimmering green.", "color": "#50C878", "slug": "nail-emerald-city", "image": "https://images.unsplash.com/photo-1518683390209-66103e351980?q=80&w=800&auto=format&fit=crop"},
        {"name": "Gold Rush", "desc": "Liquid gold finish.", "color": "#FFD700", "slug": "nail-gold-rush", "image": "https://images.unsplash.com/photo-1596462502278-27bfdd403348?q=80&w=800&auto=format&fit=crop"},
        {"name": "Silver Lining", "desc": "Chrome silver mirror effect.", "color": "#C0C0C0", "slug": "nail-silver-lining", "image": "https://images.unsplash.com/photo-1522337660859-02fbefca4702?q=80&w=800&auto=format&fit=crop"},
        {"name": "Amethyst Aura", "desc": "Holographic purple.", "color": "#9966CC", "slug": "nail-amethyst-aura", "image": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?q=80&w=800&auto=format&fit=crop"},
        {"name": "Obsidian", "desc": "Pure glossy black.", "color": "#000000", "slug": "nail-obsidian", "image": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?q=80&w=800&auto=format&fit=crop"},
        {"name": "Pearl White", "desc": "Iridescent white sheen.", "color": "#F0F8FF", "slug": "nail-pearl-white", "image": "https://images.unsplash.com/photo-1595867958652-n3-3453?q=80&w=800&auto=format&fit=crop"},
    ]

    # --- Add Perfumes ---
    for i, p in enumerate(perfumes):
        prod, created = Product.objects.update_or_create(
            slug=p['slug'],
            defaults={
                "name": p['name'],
                "description": p['desc'],
                "price": p['price'],
                "category": cat_perfume,
                "image": p['image'],
                "rating": 4.8,
                "stock": 50,
                "is_featured": True,
                "is_trending": i < 4, 
                "shades": ["Standard"]
            }
        )
        status = "Added" if created else "Updated"
        print(f"Perfume {status}: {p['name']}")

    # --- Add Nail Polishes ---
    for i, p in enumerate(nail_polishes):
        prod, created = Product.objects.update_or_create(
            slug=p['slug'],
            defaults={
                "name": f"Nail Polish - {p['name']}",
                "description": p['desc'],
                "price": 199.00,
                "category": cat_nail,
                "image": p['image'],
                "rating": 4.6,
                "stock": 100,
                "is_featured": True,
                "is_trending": i < 4,
                "shades": [p['color']]
            }
        )
        status = "Added" if created else "Updated"
        print(f"Nail Polish {status}: {p['name']}")

    print("\nDone. Products added/updated in Local Database.")

if __name__ == "__main__":
    add_live_products()
