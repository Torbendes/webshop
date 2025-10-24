from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from .models import User, Item, Review, ItemPhoto, Warehouse
from .serializers import (
    UserSerializer,
    ItemSerializer,
    ReviewSerializer,
    WarehouseSerializer,
    ItemPhotoSerializer
)


# ==============================
# Custom permission: only owner can modify
# ==============================
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    GET is allowed for everyone.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        if hasattr(obj, 'created_by'):  # Item
            return obj.created_by == request.user
        if hasattr(obj, 'reviewer'):  # Review
            return obj.reviewer == request.user

        # For other models, default deny
        return False


# ==============================
# Users
# ==============================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # alleen ingelogde users kunnen lijst zien / wijzigen


# ==============================
# Items
# ==============================
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # GET openbaar
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.created_by != self.request.user:
                raise PermissionDenied("Je kunt alleen je eigen items aanpassen/verwijderen")
        return obj


# ==============================
# Reviews
# ==============================
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # GET openbaar
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.reviewer != self.request.user:
                raise PermissionDenied("Je kunt alleen je eigen reviews aanpassen/verwijderen")
        return obj


# ==============================
# ItemPhotos
# ==============================
class ItemPhotoViewSet(viewsets.ModelViewSet):
    queryset = ItemPhoto.objects.all()
    serializer_class = ItemPhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # GET openbaar
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()


# ==============================
# Warehouses
# ==============================
class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [AllowAny]  # iedereen kan lijst zien / details
