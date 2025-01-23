from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
            'category': {'required': True},
            'stock': {'required': True},
        }

    def validate(self, data):
        # Check if the product with the same name and category already exists
        if Product.objects.filter(name=data['name'], category=data['category']).exists():
            raise serializers.ValidationError("This product already exists.")
        return data

    
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Include product details in the order item

    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'product']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='user.username', read_only=True)
    
    # Serialize Product fields in the OrderSerializer directly
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'status', 'created_at', 'items', 'total_price']
        read_only_fields = ['created_at']

    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return str(total)

