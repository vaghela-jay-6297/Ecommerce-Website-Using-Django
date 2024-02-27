# Generated by Django 5.0 on 2024-01-08 06:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_alter_user_profile_picture'),
        ('category_product_app', '0003_brand_size_product_productimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category_product_app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
    ]