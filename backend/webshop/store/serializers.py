import base64
import io
from PIL import Image
from rest_framework import serializers
from .models import User, Item, Review, ItemPhoto, Warehouse


# =========================================
# 1️⃣ User Serializer
# =========================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is verplicht.")
        return value

    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError("Username is verplicht.")
        return value


# =========================================
# 2️⃣ Item Serializer
# =========================================
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Naam is verplicht.")
        return value

    def validate_price(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Prijs moet groter dan 0 zijn.")
        return value


# =========================================
# 3️⃣ Review Serializer
# =========================================
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        review_type = data.get('review_type')
        item = data.get('item')
        reviewed_user = data.get('reviewed_user')
        reviewer = self.context['request'].user if 'request' in self.context else data.get('reviewer')

        # Type-specific requirements
        if review_type == 'item' and not item:
            raise serializers.ValidationError("Item review must have an item.")
        if review_type == 'user' and not reviewed_user:
            raise serializers.ValidationError("User review must have a reviewed_user.")
        if review_type == 'item' and reviewed_user:
            raise serializers.ValidationError("Item review cannot have a reviewed_user.")
        if review_type == 'user' and item:
            raise serializers.ValidationError("User review cannot have an item.")

        # Prevent self-review
        if review_type == 'user' and reviewer == reviewed_user:
            raise serializers.ValidationError("Een gebruiker kan zichzelf niet reviewen.")

        # Prevent duplicate reviews
        if review_type == 'item' and item and Review.objects.filter(reviewer=reviewer, item=item).exists():
            raise serializers.ValidationError("Je hebt deze item al beoordeeld.")
        if review_type == 'user' and reviewed_user and Review.objects.filter(reviewer=reviewer, reviewed_user=reviewed_user).exists():
            raise serializers.ValidationError("Je hebt deze gebruiker al beoordeeld.")

        return data

    def validate_rating(self, value):
        if value is None or not (1 <= value <= 5):
            raise serializers.ValidationError("Rating moet tussen 1 en 5 liggen.")
        return value


# =========================================
# 4️⃣ ItemPhoto Serializer
# =========================================
class ItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPhoto
        fields = ['id', 'item', 'photo_data', 'created_at']

    def validate_photo_data(self, value):
        if isinstance(value, str):
            try:
                value = base64.b64decode(value)
            except Exception:
                raise serializers.ValidationError("Invalid base64 image data")
        try:
            Image.open(io.BytesIO(value)).verify()
        except Exception:
            raise serializers.ValidationError("Invalid image file")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

# =========================================
# 5️⃣ Warehouse Serializer
# =========================================
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Naam is verplicht.")
        return value

    def validate_capacity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Capaciteit moet groter dan 0 zijn.")
        return value
