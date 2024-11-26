from django.contrib import admin

# Register your models here.
from .models import Product, Sale, Category

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Category)