# Generated by Django 5.0 on 2024-01-17 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_profile_picture'),
        ('cart_wishlist_app', '0004_discountcoupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='Null')),
                ('country', models.CharField(default='Null')),
                ('address_l1', models.TextField(default='Null')),
                ('address_l2', models.TextField(default='Null')),
                ('city', models.CharField(default='Null')),
                ('state', models.CharField(default='Null')),
                ('postcode', models.BigIntegerField(default='000000')),
                ('mobile', models.BigIntegerField(default='0000000000')),
                ('notes', models.TextField(default='Null')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
    ]
