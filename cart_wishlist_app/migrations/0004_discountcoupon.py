# Generated by Django 5.0 on 2024-01-09 07:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_profile_picture'),
        ('cart_wishlist_app', '0003_cart_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(default='Null')),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
    ]