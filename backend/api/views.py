from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem, Customer
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, WishlistSerializer, UserSerializer, OrderSerializer

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
