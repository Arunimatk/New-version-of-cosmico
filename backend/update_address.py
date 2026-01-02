
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from api.models import Order, Customer
from django.contrib.auth.models import User

def update_address():
    try:
        user = User.objects.get(username='kamala')
        print(f"Found user: {user.username}")

        # 1. Update Customer Profile (Phone & Address)
        customer, created = Customer.objects.get_or_create(user=user)
        customer.phone_number = "9876543210"
        customer.address = "Kamala, 12th Main, Indiranagar, Bangalore, 560038, India"
        customer.save()
        print("Updated Customer Profile with Phone & Address.")

        # 2. Update the Order (ID 1)
        # We can filter by user and grab the latest, or just ID 1 since we know it.
        order = Order.objects.filter(user=user).first() # Get first/latest order
        if order:
            order.shipping_address = "Kamala, 12th Main, Indiranagar, Bangalore, 560038, India"
            order.save()
            print(f"Updated Order #{order.id} with Shipping Address.")
        else:
            print("No order found for kamala.")

    except User.DoesNotExist:
        print("User 'kamala' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_address()
