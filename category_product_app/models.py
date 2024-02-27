from django.db import models
from account.models import User

""" Below Class for Category """
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, default='') # category name
    desc = models.CharField(max_length=300, default='') # category description
    slug = models.SlugField(max_length=200, unique=True, default='')    # slug is a unique for category.
    image = models.ImageField(upload_to="category", default="default.jpg")   # category image
    status = models.BooleanField(default=True)  # category status(active or not)
    created_at = models.DateTimeField(auto_now_add=True)    # Use auto_now_add for the creation time
    updated_at = models.DateTimeField(auto_now=True)    # Use auto_now for the last update time
    
    def __str__(self):
        return self.name 
    

""" All Below Class/function For Product """

""" This function create dynamic path as per different category """
def productImage_path(instance,filename):	# Create image path to save image in this folder.
	# here instance.category.name is get a name of selected category name,filename is a getting the image name by imagefield.
    return 'product/{0}/{1}'.format(instance.category.name,filename)

def subImage_path(instance,filename):	# Create image path to save image in this folder.
	# here instance.category.name is get a name of selected category name,filename is a getting the image name by imagefield.
    return 'product/{0}/{1}'.format(instance.product.category.name,filename)

# size model for product model.
class Size(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

# Brand model for product model.
class Brand(models.Model):
    name = models.CharField(max_length=50)	# Product Brand name
    status = models.BooleanField(default=True)	# brand status active or not
    def __str__(self):
        return self.name
    

# Creaete Product model to Get product details from admin and insert into database.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # get user table primary key as a foreignkey
    category = models.ForeignKey(Category,on_delete=models.CASCADE) # get category table primary key as a foreignkey
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  # product brand dropdown list
    size = models.ManyToManyField(Size)    # select multiple product size from dropdown list    
    
    name = models.CharField(max_length=200, default='') # product name
    slug = models.SlugField(max_length=200, default='', unique=True)    # product slug
    desc = models.TextField(default='', blank=True)  # product description
    
    # here in image get product_path for uploading image.
    main_image = models.ImageField(upload_to=productImage_path, default='default.jpg')    # product image
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)	# product price
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) # final product price
    
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)    # Use auto_now_add for the creation time
    updated_at = models.DateTimeField(auto_now=True)    # Use auto_now for the last update time
    
    def __str__(self):
        category = str(self.category)
        return category + ' ' + self.name
    
# ProductImage model for multiple product image.
class ProductImages(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    # subimage containg multiple images of product.
    subimage = models.ImageField(upload_to=subImage_path, default='default.jpg')
    
    def __str__(self):
        return str(self.pk) + ' ' + self.product.name 
