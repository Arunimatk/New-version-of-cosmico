from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem, Customer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [WishlistItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'get_phone', 'get_products', 'get_address', 'get_pin', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('user__username', 'full_name', 'id', 'shipping_address')
    inlines = [OrderItemInline]

    def get_phone(self, obj):
        try:
            return obj.user.customer_profile.phone_number
        except:
            return "N/A"
    get_phone.short_description = 'Phone Number'

    def get_products(self, obj):
        return ", ".join([f"{item.product.name} ({item.quantity})" for item in obj.items.all()])
    get_products.short_description = 'Products'

    def get_address(self, obj):
        return obj.shipping_address
    get_address.short_description = 'Delivery Address'

    def get_pin(self, obj):
        # Taking a simple guess that pin is often at the end or comma separated
        # User requested specific pin code logic.
        try:
             # Basic extraction if comma separated
             parts = obj.shipping_address.split(',')
             if len(parts) > 3:
                 return parts[-1]
             return "-"
        except:
            return "-"
    get_pin.short_description = 'Pin Code'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

