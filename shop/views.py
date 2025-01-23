from rest_framework import generics
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.permissions import AllowAny


# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Order Views
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        # Assign the user to the order
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        print("Fetching order with ID:", kwargs['pk'])  # Debugging line
        return super().get(request, *args, **kwargs)

