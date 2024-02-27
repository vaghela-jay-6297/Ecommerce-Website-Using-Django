from django.db import models
from account.models import User
from category_product_app.models import Product
from django.utils import timezone

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)    

    def __str__(self):
        return self.user.fname +'-' + self.product.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.CharField(default='Null')
    cart_slug = models.CharField(max_length=50, unique=True)
    qty = models.PositiveIntegerField(default=1)
    product_price = models.DecimalField(max_digits=1000, decimal_places=2)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)    # Use auto_now_add for the creation time
    updated_at = models.DateTimeField(auto_now=True)    # Use auto_now for the last update time
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        qty = str(self.qty)
        total_price = str(self.total_price)
        return self.user.fname +'-' + self.product_size + '-' + qty + '-' + total_price
    
class DiscountCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_code = models.CharField(default='Null')
    discount_amount = models.DecimalField(default=0.0, max_digits=1000, decimal_places=2)
    
    def __str__(self):
        return self.user.fname + '-' + self.coupon_code
