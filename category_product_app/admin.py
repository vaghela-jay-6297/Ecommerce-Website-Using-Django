from django.contrib import admin
from .models import Category, Size, Brand, Product, ProductImages
# Register your models here.
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductImages)
