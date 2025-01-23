from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Order, OrderItem, Product

class OrderAPITestCase(TestCase):

    def setUp(self):
        # Step 1: Create a user (admin user for the order)
        self.user = User.objects.create_user(username='admin', password='adminpassword')

        # Step 2: Create the product (Hair Dryer)
        self.product = Product.objects.create(
            name='Hair Dryer',
            description='This is a Hair Dryer.',
            price='29.99',
            category='Electronics',
            stock=10
        )

        # Step 3: Create the order with id=2 and add the product to the order items
        self.order = Order.objects.create(user=self.user, status='Shipped')

        # Create an order item and associate it with the order
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1
        )

    def test_order_detail(self):
        # Test the order detail API for the order with id=2
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Optional: Check that the order details are correct
        self.assertEqual(response.data['id'], self.order.id)
        self.assertEqual(response.data['customer_name'], 'admin')
        self.assertEqual(response.data['status'], 'Shipped')
        self.assertEqual(response.data['total_price'], '29.99')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product']['name'], 'Hair Dryer')
