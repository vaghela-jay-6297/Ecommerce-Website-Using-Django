# Generated by Django 5.0 on 2023-12-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_product_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='category'),
        ),
    ]