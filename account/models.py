from django.db import models

# Create your models here.
class User(models.Model):
    user_type=(
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller')
    )

    user_type = models.CharField(max_length=20, choices=user_type)
    fname = models.CharField(max_length=20, default='')
    lname = models.CharField(max_length=20, default='')
    email= models.EmailField(max_length=40, default='not-found', unique=True)
    mobile = models.BigIntegerField(default='0000000000')
    password = models.CharField()
    profile_picture = models.ImageField(default='default-user.png', upload_to='profile_picture/')
    created_at = models.DateTimeField(auto_now_add=True)    # Use auto_now_add for the creation time
    updated_at = models.DateTimeField(auto_now=True)    # Use auto_now for the last update time

    def __str__(self):
        return self.fname + " " + self.email