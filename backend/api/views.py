from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem, Customer
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, WishlistSerializer, UserSerializer, OrderSerializer

# ----- Utils -----
@api_view(['GET'])
def populate_products(request):
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
        {"name": "Obsidian", "desc": "Pure glossy black.", "color": "#000000", "slug": "nail-obsidian", "image": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?q=80&w=800&auto=format&fit=crop"}, # Using filler for black
        {"name": "Pearl White", "desc": "Iridescent white sheen.", "color": "#F0F8FF", "slug": "nail-pearl-white", "image": "https://images.unsplash.com/photo-1595867958652-n3-3453?q=80&w=800&auto=format&fit=crop"},
    ]

    added_count = 0

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
        if created: added_count += 1
        else: pass # Updated

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
        if created: added_count += 1
        else: pass # Updated

    return Response({"message": f"Successfully processed products. Added {added_count} new items, updated others."}, status=200)


# ----- Products -----
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=False)
    def featured(self, request):
        serializer = self.get_serializer(self.queryset.filter(is_featured=True), many=True)
        return Response(serializer.data)

    @action(detail=False)
    def trending(self, request):
        serializer = self.get_serializer(self.queryset.filter(is_trending=True), many=True)
        return Response(serializer.data)

# ----- Categories -----
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ----- Cart -----
class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response(CartSerializer(cart).data)

# ----- Wishlist -----
class WishlistViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
        if item:
            item.delete()
        else:
            WishlistItem.objects.create(wishlist=wishlist, product=product)
        return Response(WishlistSerializer(wishlist).data)

# ----- Auth -----
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        Customer.objects.create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# ----- Orders -----
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        shipping_address = request.data.get('shipping_address', 'Default Address')
        full_name = request.data.get('full_name', '')
        payment_method = request.data.get('payment_method', 'COD')
        transaction_id = request.data.get('transaction_id', None)
        
        # Determine initial payment status
        if payment_method in ['UPI', 'CARD'] and transaction_id:
             payment_status = 'Completed' # Mock success
        else:
             payment_status = 'Pending'

        if product_id:
            product = Product.objects.get(id=product_id)
            quantity = int(request.data.get('quantity', 1))
            total_price = product.price * quantity
            order = Order.objects.create(
                user=user, 
                full_name=full_name,
                total_price=total_price, 
                shipping_address=shipping_address,
                payment_method=payment_method,
                payment_status=payment_status,
                transaction_id=transaction_id
            )
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            cart, _ = Cart.objects.get_or_create(user=user)
            if not cart.items.exists():
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
            total_price = sum(item.product.price * item.quantity for item in cart.items.all())
            order = Order.objects.create(
                user=user, 
                full_name=full_name,
                total_price=total_price, 
                shipping_address=shipping_address,
                payment_method=payment_method,
                payment_status=payment_status,
                transaction_id=transaction_id
            )
            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            cart.items.all().delete()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
