from django.db import models
from datetime import date, datetime


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    low_stock_threshold = models.IntegerField(default=10)

    class Meta:
        ordering = ['name']  # Default order by name

    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    sale_date = models.DateTimeField(default=datetime.now)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    # customer_email = models.CharField(max_length=100, blank=True, null=True)
    # customer_phone = models.CharField(max_length=100, blank=True, null=True)
    # customer_address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Sale of {self.product.name} on {self.date.strftime('%Y-%m-%d')}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name
