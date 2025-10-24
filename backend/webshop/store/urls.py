from rest_framework import routers
from .views import UserViewSet, ItemViewSet, ReviewViewSet, WarehouseViewSet, EmployeeViewSet, ItemPhotoViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'itemphotos', ItemPhotoViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = router.urls
