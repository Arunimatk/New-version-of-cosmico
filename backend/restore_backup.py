import os
import json
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Product, Category

BACKUP_FILE = "products_backup.json"

def restore_products():
    if not os.path.exists(BACKUP_FILE):
        print(f"No backup file found at {BACKUP_FILE}. Skipping restoration.")
        return

    print(f"Loading products from {BACKUP_FILE}...")
    try:
        with open(BACKUP_FILE, "r", encoding='utf-8') as f:
            products_data = json.load(f)
        
        if isinstance(products_data, dict):
            if 'results' in products_data:
                products_data = products_data['results']
            else:
                 # If it's a dict but no results, maybe it's a single object or wrapper?
                 # Treat as list of one if valid, or just pass
                 pass 

        if not isinstance(products_data, list):
             print(f"Error: Expected list of products, got {type(products_data)}")
             return

        print(f"Found {len(products_data)} items in backup.") # Changed 'products' to 'items' for clarity

        updated_count = 0
        created_count = 0

        for p_data in products_data:
            # Get or create category
            cat_name = p_data.get('category_name') or (p_data.get('category') and p_data['category'].get('name')) or "Uncategorized"
            # Try to get slug from data, otherwise slugify name
            cat_slug = p_data.get('category_slug') or (p_data.get('category') and p_data['category'].get('slug')) or cat_name.lower().replace(" ", "-")
            
            category, _ = Category.objects.get_or_create(
                slug=cat_slug, 
                defaults={'name': cat_name}
            )

            # Prepare product data
            product_defaults = {
                'name': p_data.get('name'),
                'description': p_data.get('description', ''),
                'price': p_data.get('price'),
                'category': category,
                'image': p_data.get('image'), # Assuming URL or path is compatible
                'rating': p_data.get('rating', 0),
                'stock': p_data.get('stock', 0),
                'is_featured': p_data.get('is_featured', False),
                'is_trending': p_data.get('is_trending', False),
                'shades': p_data.get('shades', [])
            }

            # Use slug as unique identifier if possible, else fallback to name (?)
            # Risk: Name collisions if slug is missing. But usually slugs are reliable.
            slug = p_data.get('slug')
            if not slug:
                # If no slug, try to find by name or skip? 
                # Let's try to generate one or skip. Codebase seems to rely on slugs.
                slug = p_data.get('name', '').lower().replace(" ", "-")
            
            obj, created = Product.objects.update_or_create(
                slug=slug,
                defaults=product_defaults
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
                
        print(f"Restoration Complete. Created: {created_count}, Updated: {updated_count}")

    except Exception as e:
        print(f"Error restoring backup: {e}")

if __name__ == "__main__":
    restore_products()
