# Generated by Django 5.0.2 on 2024-11-26 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0004_category_sale_sale_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
    ]
