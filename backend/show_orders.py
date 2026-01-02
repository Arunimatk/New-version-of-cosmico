
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Order, OrderItem, Customer

def show_orders():
    orders = Order.objects.all().order_by('-created_at')
    
    print("-" * 100)
    print(f"{'ORDER ID':<10} | {'USER NAME':<15} | {'PHONE':<15} | {'TOTAL':<10} | {'STATUS':<10}")
    print("-" * 100)

    for order in orders:
        user = order.user
        
        try:
            phone = user.customer_profile.phone_number or "N/A"
        except:
            phone = "N/A"

        fullName = order.full_name if order.full_name else user.username

        print(f"{order.id:<10} | {fullName:<15} | {phone:<15} | {order.total_price:<10} | {order.status:<10}")
        
        # Parse Address
        addr_str = order.shipping_address or ""
        addr_parts = addr_str.split(',') 
        # Expecting: Name, Street, City, Zip, Country
        recipient = addr_parts[0].strip() if len(addr_parts) > 0 else "N/A"
        pin_code = addr_parts[3].strip() if len(addr_parts) > 3 else "N/A"
        
        print(f"  > Shipping Name: {recipient}")
        print(f"  > Address:       {addr_str}")
        print(f"  > Pin Code:      {pin_code}")
        
        print("  > Items:")
        items = OrderItem.objects.filter(order=order)
        for item in items:
            print(f"    - {item.product.name:<30} | Qty: {item.quantity:<5} | Price: {item.price}")
        print("-" * 100)

if __name__ == "__main__":
    show_orders()
