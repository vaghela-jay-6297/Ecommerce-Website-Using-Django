from django.db import models
from account.models import User # import models from account.models.py
from cart_wishlist_app.models import Cart, Wishlist, DiscountCoupon # import models from cart_wishlist_app.models.py
from category_product_app.models import Category, Product   # import models from category_product_app.models.py


# Create your models here.
class User_address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # get user table primary key as a foreignkey
    company_name = models.CharField(default='Null')
    country = models.CharField(default='Null')
    address_l1 = models.TextField(default='Null')
    address_l2 = models.TextField(default='Null')
    city = models.CharField(default='Null')
    state = models.CharField(default='Null')
    postcode = models.BigIntegerField(default='000000')
    mobile = models.BigIntegerField(default='0000000000')
    notes = models.TextField(default='Null')
    
    def __str__(self):
        return self.user.fname + '-' + self.city + '-' + self.state