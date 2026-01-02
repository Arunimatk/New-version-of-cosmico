import os
import django
import sys
import json

# Setup Django environment BEFORE importing serializers
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Product
from api.serializers import ProductSerializer

print("--- Serializer Test ---")
products = Product.objects.all()
# Manually serialize one item to avoid DRF setup complexity in isolated script if possible
# But ModelSerializer needs proper DRF setup.
serializer = ProductSerializer(products, many=True)
try:
    data = serializer.data
    if data:
        print(json.dumps(data[0], indent=2))
    else:
        print("No products found.")
except Exception as e:
    print(f"Error serializing: {e}")
