
import os
import django
import sys

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Cart, Wishlist, Order

def show_activity():
    users = User.objects.all().order_by('-last_login')
    
    print("\n" + "="*120)
    print(f"{'USER ACTIVITY DASHBOARD':^120}")
    print("="*120)
    
    print(f"{'USERNAME':<15} | {'LAST LOGIN':<20} | {'CART ITEMS':<12} | {'WISHLIST':<10} | {'ORDERS':<8}")
    print("-" * 120)

    for user in users:
        # User Details
        last_login = user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else "Never"
        
        # Cart Stats
        try:
            cart_count = user.cart.items.count()
            cart_items = ", ".join([item.product.name for item in user.cart.items.all()])
        except:
            cart_count = 0
            cart_items = ""

        # Wishlist Stats
        try:
            wishlist_count = user.wishlist.items.count()
            wishlist_items = ", ".join([item.product.name for item in user.wishlist.items.all()])
        except:
            wishlist_count = 0
            wishlist_items = ""

        # Order Stats
        order_count = Order.objects.filter(user=user).count()

        # Print Summary Row
        print(f"{user.username:<15} | {last_login:<20} | {str(cart_count) + ' items':<12} | {str(wishlist_count) + ' items':<10} | {order_count:<8}")

        # Print Details if any items exist
        if cart_count > 0:
            print(f"   > Cart: {cart_items}")
        if wishlist_count > 0:
            print(f"   > Wish: {wishlist_items}")
        print("-" * 120)

if __name__ == "__main__":
    show_activity()
