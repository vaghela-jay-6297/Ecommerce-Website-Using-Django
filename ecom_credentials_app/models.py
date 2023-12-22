from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    user_type=(
        ('Buyer','Buyer'),
        ('Seller','Seller')
    )
    
    user_type = models.CharField(max_length=30, choices=user_type)
    fname = models.CharField(max_length=30, default='')
    lname = models.CharField(max_length=30, default='')
    email = models.EmailField(unique=True)
    mobile = models.BigIntegerField(unique=True)
    address = models.TextField(default='')
    profile_picture = models.ImageField(default='', upload_to='profile_picture/')
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.fname + " " + self.email

class Product(models.Model):
    category=(
        ('Men','Men'),
        ('Women','Women'),
        ('Kids','Kids')
    )
    brand=(
        ('Allen Solly', 'Allen Solly'),
        ('US Polo','US Polo'),
        ('Supreme','Supreme'),
        ("Levi's", "Levi's"),
        ('Zara','Zara'),
        ('Diesel','Diesel'),
        ('Calvin Klein','Calvin Klein'),
        ('Tommy Hilfiger','Tommy Hilfiger')
    )
    size=(
        ('XS',' '),
        ('S','S'),
        ('M','M'),
        ('L','L'),
        ('XL','XL'),
        ('XXL','XXL'),
        ('XXXL','XXXL')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_category = models.CharField(choices=category)
    product_brand = models.CharField(choices=brand)
    product_size = models.CharField(choices=size)
    product_name = models.CharField(default='', max_length=200)
    product_desc = models.TextField(default='')
    product_slug = models.SlugField(default='', max_length=20)
    product_image = models.ImageField(default='', upload_to='product_picture/')
    product_price = models.FloatField(default='100')
    created_at = models.DateTimeField(auto_now_add=True)    # Use auto_now_add for the creation time
    updated_at = models.DateTimeField(auto_now=True)    # Use auto_now for the last update time

    def __str__(self):
        return self.user.fname +'-' + self.product_name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)    

    def __str__(self):
        return self.user.fname +'-' + self.product.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_slug = models.CharField(max_length=50, unique=True)
    qty = models.PositiveIntegerField(default=1)
    product_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)    # Use auto_now_add for the creation time
    updated_at = models.DateTimeField(auto_now=True)    # Use auto_now for the last update time
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        qty = str(self.qty)
        total_price = str(self.total_price)
        return self.user.fname +'-' + qty + '-' + total_price
