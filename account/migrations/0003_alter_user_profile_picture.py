# Generated by Django 5.0 on 2023-12-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='default-user.png', upload_to='profile_picture/'),
        ),
    ]
