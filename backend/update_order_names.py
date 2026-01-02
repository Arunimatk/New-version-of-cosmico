
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Order
from django.contrib.auth.models import User

def update_order_names():
    orders = Order.objects.all()
    for order in orders:
        if not order.full_name:
            # Fallback logic: Try to parse shipping address or use Username
            addr_parts = order.shipping_address.split(',') if order.shipping_address else []
            if len(addr_parts) > 0 and addr_parts[0].strip():
                order.full_name = addr_parts[0].strip()
            else:
                order.full_name = order.user.username
            order.save()
            print(f"Updated Order {order.id}: full_name set to '{order.full_name}'")

if __name__ == "__main__":
    update_order_names()
