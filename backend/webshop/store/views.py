from django.http import HttpResponse
from rest_framework import viewsets
from .models import User, Item, Review, Employee, ItemPhoto, Warehouse
from .serializers import UserSerializer, ItemSerializer, ReviewSerializer, WarehouseSerializer, EmployeeSerializer, ItemPhotoSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ItemPhotoViewSet(viewsets.ModelViewSet):
    queryset = ItemPhoto.objects.all()
    serializer_class = ItemPhotoSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer