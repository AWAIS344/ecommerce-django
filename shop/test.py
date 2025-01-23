# from django.test import TestCase
# from django.contrib.auth.models import User
# from shop.models import Order, OrderItem, Product

# class OrderAPITestCase(TestCase):

#     def setUp(self):
#         # Step 1: Create a user (admin user for the order)
#         self.user = User.objects.create_user(username='admin', password='adminpassword')

#         # Step 2: Create the product (Hair Dryer)
#         self.product = Product.objects.create(
#             name='Hair Dryer',
#             description='This is a Hair Dryer.',
#             price='29.99',
#             category='Electronics',
#             stock=10
#         )

#         # Step 3: Create the order with id=2 and add the product to the order items
#         self.order = Order.objects.create(user=self.user, status='Shipped')

#         # Create an order item and associate it with the order
#         self.order_item = OrderItem.objects.create(
#             order=self.order,
#             product=self.product,
#             quantity=1
#         )

#     def test_order_detail(self):
#         # Test the order detail API for the order with id=2
#         response = self.client.get(f'/api/orders/{self.order.id}/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response['Content-Type'], 'application/json')

#         # Optional: Check that the order details are correct
#         self.assertEqual(response.data['id'], self.order.id)
#         self.assertEqual(response.data['customer_name'], 'admin')
#         self.assertEqual(response.data['status'], 'Shipped')
#         self.assertEqual(response.data['total_price'], '29.99')
#         self.assertEqual(len(response.data['items']), 1)
#         self.assertEqual(response.data['items'][0]['product']['name'], 'Hair Dryer')

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User , re
from .models import Product, Order, OrderItem

class ProductTests(APITestCase):
    def setUp(self):
        self.product_data = {
            'name': 'Test Product',
            'description': 'A test product description.',
            'price': '19.99',
            'category': 'Test Category',
            'stock': 100
        }
        self.product_url = '/api/products/'

    def test_create_product(self):
        response = self.client.post(self.product_url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.product_data['name'])

    def test_unique_product(self):
        Product.objects.create(
            name="Unique Product",
            description="Description",
            price=19.99,
            category="Category",
            stock=10
        )

        data = {
            "name": "Unique Product",
            "description": "Description",
            "price": 19.99,
            "category": "Category",
            "stock": 10
        }
        response = self.client.post(reverse('product-list-create'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('The fields name, category must make a unique set.', str(response.data))


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(
            name='Test Product',
            description='A test product description.',
            price=19.99,
            category='Test Category',
            stock=100
        )

        self.order_url = '/api/orders/'

    def test_create_order(self):
        order_data = {
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2
                }
            ]
        }
        response = self.client.post(self.order_url, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer_name'], self.user.username)
        self.assertEqual(response.data['total_price'], '39.98')

    def test_order_total_price_calculation(self):
        order = Order.objects.create(user=self.user, status='Pending')
        OrderItem.objects.create(order=order, product=self.product, quantity=3)

        response = self.client.get(f'/api/orders/{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_price'], '59.97')


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token_url = '/api/token/'
        self.refresh_url = '/api/token/refresh/'

    def test_obtain_jwt_token(self):
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_jwt_token(self):
        token_response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        refresh_token = token_response.data['refresh']

        response = self.client.post(self.refresh_url, {
            'refresh': refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
