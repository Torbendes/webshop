from django.db import models

# Create your models here.

# =========================================
# 1️⃣ Users
# =========================================
class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional address
    street = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username

# =========================================
# 2️⃣ Warehouses
# =========================================
class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    # Address
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# =========================================
# 3️⃣ Employees
# =========================================
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    hired_at = models.DateTimeField(auto_now_add=True)
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )

    # Optional address
    street = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

# =========================================
# 4️⃣ Items
# =========================================
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# =========================================
# 5️⃣ Reviews
# =========================================
class Review(models.Model):
    REVIEW_TYPE_CHOICES = (
        ('item', 'Item'),
        ('user', 'User'),
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    reviewed_user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='reviews_received'
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews'
    )
    review_type = models.CharField(max_length=10, choices=REVIEW_TYPE_CHOICES)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensures review is either for item OR user, not both
        from django.core.exceptions import ValidationError
        if self.review_type == 'item' and not self.item:
            raise ValidationError("Item review must have an item.")
        if self.review_type == 'user' and not self.reviewed_user:
            raise ValidationError("User review must have a reviewed user.")
        if self.review_type == 'item' and self.reviewed_user:
            raise ValidationError("Item review cannot have a reviewed user.")
        if self.review_type == 'user' and self.item:
            raise ValidationError("User review cannot have an item.")

    def __str__(self):
        if self.review_type == 'item':
            return f"{self.reviewer} reviewed item {self.item}"
        return f"{self.reviewer} reviewed user {self.reviewed_user}"

# =========================================
# 6️⃣ ItemPhotos
# =========================================
class ItemPhoto(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.item.name}"
