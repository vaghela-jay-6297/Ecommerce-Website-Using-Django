# Generated by Django 4.2.7 on 2023-12-20 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_credentials_app', '0007_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_slug', models.CharField(max_length=50, unique=True)),
                ('qty', models.PositiveIntegerField(default=1)),
                ('product_price', models.FloatField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecom_credentials_app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecom_credentials_app.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Carti',
        ),
    ]
