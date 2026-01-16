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
    cat_lipstick, _ = Category.objects.get_or_create(name="lipstick", defaults={"slug": "lipstick"})
    cat_blush, _ = Category.objects.get_or_create(name="blush", defaults={"slug": "blush"})

    # --- Perfumes ---
    perfumes = [
        {"name": "Elysian Essence", "desc": "A divine blend of jasmine and sandalwood.", "price": 1250, "slug": "elysian-essence", "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?q=80&w=800&auto=format&fit=crop"},
        {"name": "Velvet Night", "desc": "Dark orchid and spices for the evening.", "price": 1400, "slug": "velvet-night", "image": "https://images.unsplash.com/photo-1594035910387-fea477942698?q=80&w=800&auto=format&fit=crop"},
        {"name": "Azure Sky", "desc": "Fresh ozone and citrus, like a clear sky.", "price": 950, "slug": "azure-sky", "image": "https://images.unsplash.com/photo-1523293188086-b431e90979ec?q=80&w=800&auto=format&fit=crop"},
        {"name": "Golden Hour", "desc": "Warm amber and vanilla, capturing the sunset.", "price": 1100, "slug": "golden-hour", "image": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?q=80&w=800&auto=format&fit=crop"},
        {"name": "Rose Quartz", "desc": "Soft rose offering a delicate floral touch.", "price": 1050, "slug": "rose-quartz", "image": "https://images.unsplash.com/photo-1583467875263-d50dec37a885?q=80&w=800&auto=format&fit=crop"},
    ]

    # --- Nail Polishes ---
    nail_polishes = [
        {"name": "Ruby Slippers", "desc": "Glittering deep red.", "color": "#E0115F", "slug": "nail-ruby-slippers", "image": "https://images.unsplash.com/photo-1632516421654-7299557b6408?q=80&w=800&auto=format&fit=crop"},
        {"name": "Sapphire star", "desc": "Metallic heavy blue.", "color": "#0F52BA", "slug": "nail-sapphire-star", "image": "https://images.unsplash.com/photo-1604654894610-df63bc536371?q=80&w=800&auto=format&fit=crop"},
        {"name": "Emerald City", "desc": "Shimmering green.", "color": "#50C878", "slug": "nail-emerald-city", "image": "https://images.unsplash.com/photo-1518683390209-66103e351980?q=80&w=800&auto=format&fit=crop"},
        {"name": "Gold Rush", "desc": "Liquid gold finish.", "color": "#FFD700", "slug": "nail-gold-rush", "image": "https://images.unsplash.com/photo-1596462502278-27bfdd403348?q=80&w=800&auto=format&fit=crop"},
        {"name": "Silver Lining", "desc": "Chrome silver mirror effect.", "color": "#C0C0C0", "slug": "nail-silver-lining", "image": "https://images.unsplash.com/photo-1522337660859-02fbefca4702?q=80&w=800&auto=format&fit=crop"},
    ]

    # --- Lipsticks ---
    lipsticks = [
        {"name": "Classic Red", "desc": "Matte finish bold red.", "color": "#DC143C", "slug": "lip-classic-red", "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?q=80&w=800&auto=format&fit=crop"},
        {"name": "Nude Rose", "desc": "Creamy everyday nude.", "color": "#BC8F8F", "slug": "lip-nude-rose", "image": "https://images.unsplash.com/photo-1627918543787-82787836166a?q=80&w=800&auto=format&fit=crop"},
        {"name": "Berry Crush", "desc": "Deep berry stain.", "color": "#800080", "slug": "lip-berry-crush", "image": "https://images.unsplash.com/photo-1625093742435-09c6ac4e93e0?q=80&w=800&auto=format&fit=crop"},
        {"name": "Coral Reef", "desc": "Bright summer orange.", "color": "#FF7F50", "slug": "lip-coral-reef", "image": "https://images.unsplash.com/photo-1591360236480-949449e793e7?q=80&w=800&auto=format&fit=crop"},
    ]

    # --- Blushes ---
    blushes = [
        {"name": "Peachy Keen", "desc": "Soft peach glow.", "color": "#FFDAB9", "slug": "blush-peachy-keen", "image": "https://images.unsplash.com/photo-1515688594390-b649af70d282?q=80&w=800&auto=format&fit=crop"},
        {"name": "Rose Petal", "desc": "Natural pink flush.", "color": "#FFB6C1", "slug": "blush-rose-petal", "image": "https://images.unsplash.com/photo-1596704017235-d9147565d7dd?q=80&w=800&auto=format&fit=crop"},
        {"name": "Bronze Goddess", "desc": "Sun-kissed bronze.", "color": "#CD7F32", "slug": "blush-bronze-goddess", "image": "https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?q=80&w=800&auto=format&fit=crop"},
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
                "is_trending": True, 
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
                "is_trending": True,
                "shades": [p['color']]
            }
        )
        status = "Added" if created else "Updated"
        print(f"Nail Polish {status}: {p['name']}")

    # --- Add Lipsticks ---
    for i, p in enumerate(lipsticks):
        prod, created = Product.objects.update_or_create(
            slug=p['slug'],
            defaults={
                "name": f"Lipstick - {p['name']}",
                "description": p['desc'],
                "price": 450.00,
                "category": cat_lipstick,
                "image": p['image'],
                "rating": 4.7,
                "stock": 80,
                "is_featured": True,
                "is_trending": True,
                "shades": [p['color']]
            }
        )
        status = "Added" if created else "Updated"
        print(f"Lipstick {status}: {p['name']}")

    # --- Add Blushes ---
    for i, p in enumerate(blushes):
        prod, created = Product.objects.update_or_create(
            slug=p['slug'],
            defaults={
                "name": f"Blush - {p['name']}",
                "description": p['desc'],
                "price": 550.00,
                "category": cat_blush,
                "image": p['image'],
                "rating": 4.5,
                "stock": 60,
                "is_featured": True,
                "is_trending": True,
                "shades": [p['color']]
            }
        )
        status = "Added" if created else "Updated"
        print(f"Blush {status}: {p['name']}")

    print("\nDone. Products added/updated in Local Database.")

if __name__ == "__main__":
    add_live_products()
