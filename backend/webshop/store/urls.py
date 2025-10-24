from rest_framework import routers
from .views import UserViewSet, ItemViewSet, ReviewViewSet, WarehouseViewSet, ItemPhotoViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'itemphotos', ItemPhotoViewSet)

urlpatterns = router.urls
