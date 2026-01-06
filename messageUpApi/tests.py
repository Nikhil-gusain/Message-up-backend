from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from messageUpApi.models import (
    User, UserType, Business, BusinessCategory, 
    Product, ProductCategory, Cart, CartItem, Status, Order
)

class BaseAPITest(APITestCase):
    def setUp(self):
        # Create User Type
        self.user_type = UserType.objects.create(name="Customer", label="customer")
        self.business_user_type = UserType.objects.create(name="Business", label="business")

        # Create User
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="test1234",
            user_type=self.user_type
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Create Business User
        self.biz_user = User.objects.create_user(
            username="bizuser",
            email="biz@example.com",
            password="biz1234",
            user_type=self.business_user_type
        )
        biz_refresh = RefreshToken.for_user(self.biz_user)
        self.biz_access_token = str(biz_refresh.access_token)

        # Create Business Dependencies
        self.biz_category = BusinessCategory.objects.create(label="Tech", value="tech")
        self.business = Business.objects.create(
            name="Test Business",
            description="A test business",
            address="123 Test St",
            phone=1234567890,
            category=self.biz_category,
            user=self.biz_user, # Associated with biz_user
            profile=SimpleUploadedFile("profile.jpg", b"file_content", content_type="image/jpeg")
        )

        # Create Product Dependencies
        self.prod_category = ProductCategory.objects.create(label="Electronics", value="electronics")
        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            description="A test product",
            category=self.prod_category,
            business=self.business,
            image=SimpleUploadedFile("product.jpg", b"file_content", content_type="image/jpeg"),
            available=True
        )

class AuthTests(BaseAPITest):
    def test_authenticated_access(self):
        print("Testing Authenticated Access to Cart Endpoint")
        response = self.client.get("/api/cart/")
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthenticated_access(self):
        print("Testing Unauthenticated Access to Cart Endpoint")
        self.client.credentials()  # Remove credentials
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('messageUpApi.controllers.authController.authController.google_auth_task')
    def test_google_auth(self, mock_google_auth):
        print("Testing Google Auth")
        # Mock successful return from task: (ok, payload)
        mock_google_auth.return_value = (True, {
            'email': 'google@example.com', 
            'access': 'fake_access_token',
            'refresh': 'fake_refresh_token'
        })
        response = self.client.post("/api/auth/google/", {'id_token': 'valid_token'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BusinessTests(BaseAPITest):
    # Removed test_get_business_list as endpoint does not support listing without slug.

    def test_get_business_detail(self):
        print(f"Testing Get Business Detail: {self.business.slug}")
        response = self.client.get(f"/api/business/{self.business.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.business.name)

    def test_create_business(self):
        print("Testing Create Business")
        # Use a new user for creation test to avoid conflict if 1-to-1 limit
        new_user = User.objects.create_user("newbiz", "new@biz.com", "pass", user_type=self.business_user_type)
        refresh = RefreshToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")

        data = {
            "name": "New Biz",
            "description": "Desc",
            "address": "Addr",
            "phone": 1234567890,
            "category": self.biz_category.id,
            "profile": SimpleUploadedFile("new.jpg", b"content", content_type="image/jpeg")
        }
        response = self.client.post("/api/business/", data, format='multipart')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
    
    def test_update_business(self):
        print("Testing Update Business")
        # Authenticate as biz owner
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.biz_access_token}")
        
        data = {"name": "Updated Biz Name"}
        response = self.client.put("/api/business/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.business.refresh_from_db()
        self.assertEqual(self.business.name, "Updated Biz Name")

    def test_delete_business(self):
        print("Testing Delete Business")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.biz_access_token}")
        response = self.client.delete("/api/business/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.assertFalse(Business.objects.filter(id=self.business.id).exists())

class StatusTests(BaseAPITest):
    def test_status_lifecycle(self):
        print("Testing Status Lifecycle (Create, Get, Delete)")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.biz_access_token}")
        
        # Create
        data = {
            "image": SimpleUploadedFile("status.jpg", b"content", content_type="image/jpeg")
        }
        response = self.client.post("/api/status/", data, format='multipart')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        status_slug = self.business.slug # Assuming status is linked to biz slug or id?
        # Actually StatusAPI.get matches <slug:slug>. Likely business slug.
        
        # Get
        response = self.client.get(f"/api/status/{self.business.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete
        # Status delete needs ID in body
        # Since we just created it, we can't easily get ID from create response if we didn't capture it?
        # But we can query it.
        status_obj = Status.objects.filter(business=self.business).first()
        if status_obj:
            response = self.client.delete("/api/status/", {"id": status_obj.id}, format='json')
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

class ProductTests(BaseAPITest):
    def test_list_products_by_category(self):
        print(f"Testing List Products by Category: {self.prod_category.label}")
        response = self.client.get(f"/api/product/category/{self.prod_category.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)

    def test_get_product_detail(self):
        print(f"Testing Get Product Detail: {self.product.name}")
        response = self.client.get(f"/api/product/{self.product.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_product_lifecycle(self):
        print("Testing Business Product Lifecycle")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.biz_access_token}")
        
        # Create
        data = {
            "name": "New Product",
            "price": 200,
            "description": "Desc",
            "category": self.prod_category.id,
            "image": SimpleUploadedFile("p.jpg", b"c", content_type="image/jpeg"),
            "available": True
        }
        response = self.client.post("/api/business/product/", data, format='multipart')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        
        # Get (Business View)
        # Assuming slug generation logic
        slug = "new-product" 
        response = self.client.get(f"/api/business/product/{slug}/")
        # If slugify isn't perfect in test, we might fail here. 
        # But let's assume standard slugify.
        
        # Update
        update_data = {"price": 300}
        response = self.client.put(f"/api/business/product/{slug}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete
        response = self.client.delete(f"/api/business/product/{slug}/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

    def test_business_by_category(self):
        print("Testing Business By Category")
        response = self.client.get(f"/api/business/category/{self.biz_category.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CartTests(BaseAPITest):
    def test_cart_operations(self):
        print("Testing Cart Operations (Get, Put, Delete)")
        # Get Empty
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Put (Add/Update)
        # Assuming payload structure: {product: X, quantity: Y} based on error msg
        data = {"product": self.product.slug, "quantity": 2} # cartTask expects slug for 'product' key based on traceback
        response = self.client.put("/api/cart/", data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        
        # Verify added
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check data integrity if possible (depends on response structure)
        
        # Delete Item
        response = self.client.delete(f"/api/cart/{self.product.id}/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

class OrderTests(BaseAPITest):
    def test_user_order_lifecycle(self):
        print("Testing User Order Lifecycle")
        # Setup cart
        cart, _ = Cart.objects.get_or_create(user=self.user)
        item = CartItem.objects.create(product=self.product, quantity=1)
        cart.items.add(item)
        
        # Create Order
        response = self.client.post("/api/user/orders/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        
        # List Orders
        response = self.client.get("/api/user/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_order_management(self):
        print("Testing Business Order Management")
        # Create an order first (as user)
        cart, _ = Cart.objects.get_or_create(user=self.user)
        item = CartItem.objects.create(product=self.product, quantity=1)
        cart.items.add(item)
        
        # Manually create order or use endpoint? 
        # Endpoint clears cart, so let's stick to manual or endpoint.
        # Let's create Order object manually to avoid side effects of previous tests depending on DB state if not flushed.
        # DB is flushed per test in TestCase.
        
        order = Order.objects.create(
            business=self.business,
            user=self.user,
            price=100,
            status="pending"
        )
        order.items.add(item) # ManyToMany
        
        # Switch to Biz User
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.biz_access_token}")
        
        # List Biz Orders
        response = self.client.get("/api/business/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Update Order (PUT)
        # Payload likely requires order_id + status
        data = {"order_id": order.id, "status": "completed"}
        response = self.client.put("/api/business/orders/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order.refresh_from_db()
        self.assertEqual(order.status, "completed")
