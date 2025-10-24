from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Warehouse, Item, Review, ItemPhoto

admin.site.register(User)
admin.site.register(Warehouse)
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(ItemPhoto)
