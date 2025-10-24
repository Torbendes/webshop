import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from store.models import User, Warehouse, Item, Review, ItemPhoto
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Seed the database with test data for Users, Warehouses, Items, Reviews, and ItemPhotos.'

    def handle(self, *args, **kwargs):
        # -----------------------
        # 1️⃣ Users
        # -----------------------
        users = []
        self.stdout.write("📌 Creating users...")
        for i in range(1, 6):
            u = User.objects.create_user(
                email=f"user{i}@example.com",
                username=f"user{i}",
                password="pass123",
                first_name=f"First{i}",
                last_name=f"Last{i}"
            )
            users.append(u)
        self.stdout.write(f"✅ Created {len(users)} users.")

        # -----------------------
        # 2️⃣ Warehouses
        # -----------------------
        warehouses = []
        self.stdout.write("📌 Creating warehouses...")
        for i in range(1, 4):
            w = Warehouse.objects.create(
                name=f"Warehouse {i}",
                street=f"Street {i}",
                house_number=str(i),
                postal_code=f"100{i}",
                city="City",
                country="Country",
                capacity=random.randint(50, 200)
            )
            warehouses.append(w)
        self.stdout.write(f"✅ Created {len(warehouses)} warehouses.")

        # -----------------------
        # 3️⃣ Items
        # -----------------------
        items = []
        self.stdout.write("📌 Creating items...")
        for i in range(1, 11):
            item = Item.objects.create(
                name=f"Item {i}",
                description=f"Description for item {i}",
                price=Decimal(f"{random.uniform(5, 100):.2f}"),
                created_by=random.choice(users),
                is_available=random.choice([True, False])
            )
            items.append(item)
        self.stdout.write(f"✅ Created {len(items)} items.")

        # -----------------------
        # 4️⃣ Reviews
        # -----------------------
        self.stdout.write("📌 Creating item reviews...")
        for i in range(10):
            try:
                Review.objects.create(
                    reviewer=random.choice(users),
                    item=random.choice(items),
                    review_type="item",
                    rating=random.randint(1, 5),
                    comment=f"Review comment {i} for item"
                )
            except IntegrityError:
                continue  # skip duplicate

        self.stdout.write("📌 Creating user reviews...")
        for i in range(5):
            try:
                reviewer, reviewed_user = random.sample(users, 2)
                Review.objects.create(
                    reviewer=reviewer,
                    reviewed_user=reviewed_user,
                    review_type="user",
                    rating=random.randint(1, 5),
                    comment=f"Review comment {i} for user"
                )
            except IntegrityError:
                continue  # skip duplicate

        self.stdout.write(f"✅ Total reviews: {Review.objects.count()}")

        # -----------------------
        # 5️⃣ ItemPhotos
        # -----------------------
        self.stdout.write("📌 Creating item photos...")
        dummy_image = b'\x89PNG\r\n\x1a\n...'  # voorbeeld binaire data
        for item in items:
            ItemPhoto.objects.create(
                item=item,
                photo_data=dummy_image
            )
        self.stdout.write(f"✅ Total item photos: {ItemPhoto.objects.count()}")

        self.stdout.write("🎉 All test data successfully created!")
