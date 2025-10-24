import base64
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from store.models import User, Item, Review, Warehouse, ItemPhoto


class StoreAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # ----------------------
        # Users
        # ----------------------
        self.user1 = User.objects.create_user(
            email="user1@example.com", username="user1", password="pass123"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", username="user2", password="pass123"
        )

        # ----------------------
        # Warehouses
        # ----------------------
        self.warehouse1 = Warehouse.objects.create(
            name="WH1", street="Street 1", house_number="1",
            postal_code="1000", city="City", country="Country", capacity=100
        )

        # ----------------------
        # Items
        # ----------------------
        self.item1 = Item.objects.create(
            name="Item 1", price=10.0, created_by=self.user1, is_available=True
        )
        self.item2 = Item.objects.create(
            name="Item 2", price=20.0, created_by=self.user2, is_available=False
        )

        # ----------------------
        # ItemPhoto
        # ----------------------
        self.photo_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgF9sFygAAAAASUVORK5CYII="
        )
        self.photo1 = ItemPhoto.objects.create(item=self.item1, photo_data=self.photo_data)

        # ----------------------
        # Reviews (avoid UNIQUE conflicts)
        # ----------------------
        self.review_item1_user1 = Review.objects.create(
            reviewer=self.user1,
            item=self.item2,  # user1 reviews item2
            review_type="item",
            rating=4,
            comment="Nice item"
        )
        self.review_user1_user2 = Review.objects.create(
            reviewer=self.user1,
            reviewed_user=self.user2,
            review_type="user",
            rating=5,
            comment="Excellent user"
        )

    # ----------------------
    # Users
    # ----------------------
    def test_user_count(self):
        self.assertEqual(User.objects.count(), 2)

    # ----------------------
    # Items
    # ----------------------
    def test_get_items_list(self):
        url = reverse('item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_item_detail(self):
        url = reverse('item-detail', args=[self.item1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item1.name)

    def test_create_item_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('item-list')
        data = {"name": "Item 3", "price": 30.0, "is_available": True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 3)

    def test_anonymous_cannot_create_item(self):
        self.client.force_authenticate(user=None)
        url = reverse('item-list')
        data = {"name": "Item X", "price": 50.0, "is_available": True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----------------------
    # Reviews
    # ----------------------

    def test_anonymous_cannot_create_review(self):
        self.client.force_authenticate(user=None)
        url = reverse('review-list')
        data = {
            "item": self.item1.id,
            "review_type": "item",
            "rating": 4,
            "comment": "Nice!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_validation_item_without_item(self):
        """Item review must have an item."""
        self.client.force_authenticate(user=self.user2)
        url = reverse('review-list')
        data = {
            "review_type": "item",
            "rating": 3,
            "comment": "Invalid review"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_validation_user_without_user(self):
        """User review must have reviewed_user."""
        self.client.force_authenticate(user=self.user2)
        url = reverse('review-list')
        data = {
            "review_type": "user",
            "rating": 5,
            "comment": "Invalid review"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_review_self(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('review-list')
        data = {
            "review_type": "user",
            "reviewed_user": self.user1.id,
            "rating": 5,
            "comment": "Self review!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_must_be_1_to_5(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('review-list')
        data = {
            "item": self.item1.id,
            "review_type": "item",
            "rating": 6,
            "comment": "Too high rating"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_required(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('review-list')
        data = {
            "item": self.item1.id,
            "review_type": "item",
            "rating": 4,
            "comment": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ----------------------
    # Item Validations
    # ----------------------
    def test_item_must_have_price(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('item-list')
        data = {"name": "Invalid Item", "is_available": True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_item_price_must_be_positive(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('item-list')
        data = {"name": "Free Item", "price": -5.0, "is_available": True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ----------------------
    # Warehouse Validations
    # ----------------------
    def test_warehouse_capacity_positive(self):
        url = reverse('warehouse-list')
        data = {
            "name": "WH2", "street": "Street 2", "house_number": "2",
            "postal_code": "2000", "city": "City2", "country": "Country",
            "capacity": 0
        }
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ----------------------
    # ItemPhoto Validations
    # ----------------------
    def test_create_itemphoto_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('itemphoto-list')
        data = {
            "item": self.item2.id,
            "photo_data": base64.b64encode(self.photo_data).decode('utf-8')
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.item2.photos.count(), 1)

    # ----------------------
    # Warehouses GET
    # ----------------------
    def test_get_warehouses_list(self):
        url = reverse('warehouse-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_warehouse_detail(self):
        url = reverse('warehouse-detail', args=[self.warehouse1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.warehouse1.name)

    # ----------------------
    # Items GET
    # ----------------------
    def test_get_itemphotos_list(self):
        url = reverse('itemphoto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
