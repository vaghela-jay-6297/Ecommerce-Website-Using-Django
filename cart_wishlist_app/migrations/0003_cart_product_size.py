# Generated by Django 5.0 on 2024-01-08 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_wishlist_app', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product_size',
            field=models.CharField(default='Null'),
        ),
    ]
