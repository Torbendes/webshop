from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import imghdr

# =========================================
# 1️⃣ Custom User Manager
# =========================================
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.is_active = extra_fields.get('is_active', True)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


# =========================================
# 2️⃣ User model
# =========================================
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional address
    street = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    # Django auth fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# =========================================
# 3️⃣ Warehouses
# =========================================
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.name} ({self.city})"


# =========================================
# 4️⃣ Items
# =========================================
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
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

    def main_photo(self):
        return self.photos.first()

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be greater than zero.")


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
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # type-based checks
        if self.review_type == 'item':
            if not self.item:
                raise ValidationError("Item review must have an item.")
            if self.reviewed_user:
                raise ValidationError("Item review cannot have a reviewed user.")
        elif self.review_type == 'user':
            if not self.reviewed_user:
                raise ValidationError("User review must have a reviewed_user.")
            if self.item:
                raise ValidationError("User review cannot have an item.")
            if self.reviewer == self.reviewed_user:
                raise ValidationError("Reviewer cannot review themselves.")
        # comment must be present
        if not self.comment or self.comment.strip() == "":
            raise ValidationError("Comment is required.")

    def __str__(self):
        if self.review_type == 'item':
            return f"{self.reviewer} reviewed item {self.item}"
        return f"{self.reviewer} reviewed user {self.reviewed_user}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reviewer', 'item'], name='unique_item_review'),
            models.UniqueConstraint(fields=['reviewer', 'reviewed_user'], name='unique_user_review'),
        ]


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

    def clean(self):
        # check if binary data is actually an image
        if imghdr.what(None, h=self.photo_data) is None:
            raise ValidationError("Uploaded data must be a valid image.")

    def __str__(self):
        return f"Photo of {self.item.name}"
