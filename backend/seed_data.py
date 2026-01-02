import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Category, Product
from django.core.files.base import ContentFile

def seed():
    # Clear existing
    Category.objects.all().delete()
    Product.objects.all().delete()
    
    categories_data = [
        {'name': 'Lipstick', 'slug': 'lipstick'},
        {'name': 'Foundation', 'slug': 'foundation'},
        {'name': 'Perfume', 'slug': 'perfume'},
        {'name': 'Blush', 'slug': 'blush'},
    ]
    
    cats = {}
    for c in categories_data:
        cat = Category.objects.create(name=c['name'], slug=c['slug'])
        cats[c['slug']] = cat
        print(f"Created category: {cat.name}")

    products_data = [
        {
            'category': 'lipstick',
            'name': 'Velvet Rose Matte',
            'price': 25.00,
            'description': 'A rich, long-lasting matte lipstick in a deep rose shade. Enriched with Vitamin E for hydration.',
            'shades': ['#B2575D', '#9A3B43', '#802A32'],
            'is_featured': True
        },
        {
            'category': 'lipstick',
            'name': 'Nude Silk Creme',
            'price': 22.00,
            'description': 'Creamy, lightweight nude lipstick that glides on effortlessly. Perfect for everyday wear.',
            'shades': ['#D4A190', '#C58C7A'],
            'is_trending': True
        },
        {
            'category': 'lipstick',
            'name': 'Ruby Red Shine',
            'price': 28.00,
            'description': 'High-gloss red lipstick for a bold statement look. Non-sticky formula.',
            'shades': ['#E60000']
        },
        {
            'category': 'foundation',
            'name': 'Flawless Skin Liquid',
            'price': 45.00,
            'description': 'Full coverage liquid foundation with a natural matte finish. 24-hour wear.',
            'shades': ['#F3E5DC', '#EACFB9', '#D1A687', '#8D5E42'],
            'is_featured': True
        },
        {
            'category': 'foundation',
            'name': 'Glow Cushion Compact',
            'price': 38.00,
            'description': 'Hydrating cushion foundation for a dewy, radiant glow. SPF 30 protected.',
            'shades': ['#F5E6DA', '#DBBCAA'],
            'is_trending': True
        },
        {
            'category': 'perfume',
            'name': 'Midnight Bloom',
            'price': 85.00,
            'description': 'An enchanting blend of jasmine, tuberose, and vanilla. Sensual and mysterious.',
            'shades': [],
            'is_featured': True
        },
        {
            'category': 'perfume',
            'name': 'Rose Gardenia',
            'price': 75.00,
            'description': 'Fresh floral scent with notes of rose petals and gardenia. Light and airy.',
            'shades': []
        },
        {
            'category': 'blush',
            'name': 'Peachy Keen Powder',
            'price': 30.00,
            'description': 'Soft peach tones to add warmth to your complexion. Buildable color.',
            'shades': ['#FFCBA4'],
            'is_trending': True
        },
        {
            'category': 'blush',
            'name': 'Rosy Cheeks Stain',
            'price': 26.00,
            'description': 'Liquid blush stain for a natural flush that lasts all day.',
            'shades': ['#FF9999']
        }
    ]

    for p in products_data:
        cat = cats[p['category']]
        prod = Product.objects.create(
            category=cat,
            name=p['name'],
            slug=p['name'].lower().replace(' ', '-'),
            description=p['description'],
            price=p['price'],
            rating=item_rating(4.0, 5.0),
            stock=100,
            shades=p['shades'],
            is_featured=p.get('is_featured', False),
            is_trending=p.get('is_trending', False)
        )
        print(f"Created product: {prod.name}")

def item_rating(min_r, max_r):
    return round(random.uniform(min_r, max_r), 1)

if __name__ == '__main__':
    seed()
