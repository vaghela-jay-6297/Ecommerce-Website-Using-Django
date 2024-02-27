from django.shortcuts import render, redirect
from account.models import User # get User model from models.py of account app
from .models import Category, Brand, Size, ProductImages, Product    # get model from models.py file
from cart_wishlist_app.models import Wishlist # get Wishlist model from models.py of cart_wishlist_app app
from django.utils.crypto import get_random_string   # generate slug value of product


# Create your views here.

''' Seller User Function '''
def add_category(request):  # this function seller can add categories
    if request.method == "POST":    # check html form request.
        try:
            Category.objects.get(name=request.POST['name']) # get category object when name is found in DB
            warning = "Category Already Added! Please Check."  # warning message
            return render(request, 'seller/category/seller-add-category.html', {'warning':warning})   
        except:
            desc, status = 'Null', False # set variable
            if request.POST['desc'] != '':  # check desc varible is not empty than set get string from Form data.
                desc =  request.POST['desc']    # set status value
            if request.POST['status'] == 'on':  # check status value is on then set True
                status = True  # set status value                

            slug = get_random_string(length=12) # generate 12 character unique slug
            try:    # if image found then insert image into table 
                # create category object in table.
                Category.objects.create(name=request.POST['name'],
                                        desc=desc,
                                        slug=slug,
                                        image=request.FILES['image'],
                                        status=status)
            except Exception as e:
                print("Exception Found: ", e)

            success = "Category Successfully Added!"  # success message
            return render(request, 'seller/category/seller-add-category.html', {'success':success})          
    else:
        return render(request, 'seller/category/seller-add-category.html')
     
def del_up_category(request):   # in this function show product in tables with action button of update & delete
    try:
        # category = Category.objects.filter(status=True) # fetch all category thrie status is true.
        category = Category.objects.all()
        return render(request, 'seller/category/seller-del-up-category.html',{'category':category})
    except Exception as e:
        print("Exception Found: ", e)
    
def drop_category(request, slug):   # in this function seller can drop category
    try:
        category = Category.objects.get(slug=slug) # get single object when slug value is equal to slug
        category.delete()   # delete that category
        return redirect('del-up-category')
    except Exception as e:
        print("Exception Found: ", e)

def update_category(request, slug): # in this function seller can update category
    try:    # try to get single object by slug
        category = Category.objects.get(slug=slug)  # get object filtering by slug
        if request.method == 'POST':    # check request method
            status = True   # set status varibale 
            if request.POST.get('update-status') == None:  # check status value is None 
                status = False  # set status value false
            category.name = request.POST['update-name'] # update category name  
            category.desc = request.POST['update-desc'] # update category description
            category.status = status    # update category status
            try:    # try to get image
                category.image = request.FILES['update-image']  # update category image
            except: # occure when image is not found
                pass
            category.save() # save category data
            return redirect('del-up-category')
        else:   # request methods is not post
            return render(request, 'seller/category/seller-update-category.html', {'category':category})
    except Exception as e:
        print("Exception Found: ", e)
        
def add_product(request):   # in this function seller can add product 
    if request.method == 'POST':
        slug = get_random_string(length=24) # generate slug value of 24 character.
        desc, status = 'Null', False # set variable
        if request.POST['product-desc'] != '':  # check desc varible is not empty than set get string from Form data.
            desc =  request.POST['product-desc']    # set status value
        if request.POST['product-status'] == 'on':  # check status value is on then set True
            status = True  # set status value      

        try:
            user = User.objects.get(email=request.session['email']) # get logged in user email by session
            category = Category.objects.get(name=request.POST["category"])  # get user's selected category name
            brand = Brand.objects.get(name=request.POST["brand"])   # get user's selected brand name            
            sizes = request.POST.getlist("product-size")    # get multiple values from user-side
            product=Product.objects.create(user=user,   # create product in table
                                   category=category,
                                   brand=brand,
                                   name=request.POST["product-name"],
                                   slug=slug,
                                   main_image=request.FILES["main-image"],
                                   desc=desc,
                                   price=request.POST["price"],
                                   offer_price=request.POST["offer-price"],
                                   available=status)
            product.size.set(sizes)  # here assign multiple values to size field of product table
            
            """ Insert Multiple images of single product """
            for image in request.FILES.getlist('sub-images'):   # Handle image uploads
                # insert multiple images in ProductImage this table connect with product table.
                ProductImages.objects.create(subimage=image, product=product)

            return redirect('view-del-up-product')
        except Exception as e:
            print("Exception Found: ", e)
    else:
        try:    # tring category data found then execute try block otherwise execute except block.
            # get only name column data. When flat=True is used, the result will be a flat list containing only the values otherwise result would be a list of tuples
            category_name = list(Category.objects.values_list('name', flat=True))
            brand = Brand.objects.filter(status=True)   # get only that brand their status is True
            size=Size.objects.all() # get all data/object from size table.
            return render(request, 'seller/product/seller-add-product.html', {'category_name':category_name, 'brand':brand, 'size':size})
        except:
            return render(request, 'seller/product/seller-add-product.html')

def view_del_up_product(request):   # seller view-delete-update product. show data in table.
    try:
        user = User.objects.get(email=request.session['email']) # get logged in user object
        product = Product.objects.filter(user=user) # filter product user wise
        return render(request, 'seller/product/seller-view-del-up-product.html', {'product':product})
    except Exception as e:
        return render(request, 'error-404.html')

def view_product(request, slug):  # seller can View/show their product. single product.
    try:
        user = User.objects.get(email=request.session['email']) # get logged in user object
        product = Product.objects.get(user=user, slug=slug) # get product by user, slug wise.
        productImages = ProductImages.objects.filter(product=product) # filter product images by product foreign key
        return render(request, 'seller/product/seller-view-product.html', {'product':product, 'productImages':productImages})
    except Exception as e:
        return render(request, 'error-404.html')

def update_product(request, slug):    # seller can Update their product.
    try:
        product = Product.objects.get(slug=slug)    # get product by user, slug wise.
        category = Category.objects.all()   # get all categories
        brand = Brand.objects.all()  # get all brands
        size = Size.objects.all()   # get all sizes
        if request.method == "POST":    # check form http method
            avilable = True   # set status varibale 
            if request.POST.get('update-status') == None:  # check status value is None 
                avilable = False  # set status value false
            else:
                pass
            
            if request.POST.get('new-category') != None:     # check new-category is None or not
                category = Category.objects.get(name=request.POST['new-category'])  # get new-category value from userside
                product.category = category # update category
                
            if request.POST.get('new-brand') != None:   # check new-brand is None or not
                brand = Brand.objects.get(name=request.POST['new-brand'])   # get new-brand value from userside
                product.brand = brand   # update brand
            
            if request.POST.getlist('new-size'):    # check new-size list Empty or not
                size = request.POST.getlist('new-size') # get new-size list
                product.size.set(size)  # update size
            
            if request.FILES.get('new-main-image') != None: # check new-main-image is None or not
                product.main_image = request.FILES['new-main-image']    # update main_image
                
            product.name = request.POST['new-name'] # get new-name & update it
            product.desc = request.POST['new-desc'] # get new-desc & update it
            product.price = request.POST['new-price']   # get new-price & update it
            product.offer_price = request.POST['new-offer-price']   # get new-offer-price & update it
            product.available = avilable    # update avilable boolean field
            product.save()  # save data
            
            if request.FILES.getlist('new-sub-images') != None: # check new-sub-images list is None or not
                productimage = ProductImages.objects.filter(product=product)    # filter ProductImages by product
                productimage.delete()   # delete those images
                """ Insert Multiple images of single product """
                for image in request.FILES.getlist('new-sub-images'):   # Handle image uploads
                    # insert multiple images in ProductImage this table connect with product table.
                    ProductImages.objects.create(subimage=image, product=product)  
                
            return redirect('view-del-up-product')                
        else:
            return render(request, 'seller/product/seller-update-product.html', {'product':product, 'category':category, 'brand':brand, 'size':size})
    except Exception as e:
        print("Exception Found:",e)    

def drop_product(request, slug):    # seller can delete their product
    try:
        product =  Product.objects.get(slug=slug)   # get product object by slug.
        product.delete()    # delete product object 
        return redirect('view-del-up-product')
    except Exception as e:
        return render(request, 'error-404.html')

''' End Seller User Function '''


''' Buyer User Function '''
def category(request):  # fetch all categories
    category_l1 = Category.objects.all()[:6]    # first 6 categories in category_l1
    category_l2 = Category.objects.all()[6:]    # start from 6th index to end categories in category_l2
    return render(request, 'buyer/category.html', {'category_l1':category_l1, 'category_l2':category_l2})

def product_by_category(request, category_name):    # get all products filter by category
    category_l1 = Category.objects.all()[:6]    # first 6 categories in category_l1
    category_l2 = Category.objects.all()[6:]    # start from 6th index to end categories in category_l2
    wishlist_flag = False   # create a wishlist_flag boolean variable with default False Value.
    try:
        category = Category.objects.get(name=category_name) # get category object.
        products = Product.objects.filter(category=category) # fetch product filter by category.
        return render(request, 'buyer/product-by-category.html', {'products':products,'category_l1':category_l1,'category_l2':category_l2})
    except:
        return render(request, 'error-404.html')

def product_all(request):
    category_l1 = Category.objects.all()[:6]    # first 6 categories in category_l1
    category_l2 = Category.objects.all()[6:]    # start from 6th index to end categories in category_l2
    wishlist_flag = False   # create a wishlist_flag boolean variable with default False Value.
    
    try:
        products = Product.objects.filter(available=True)
        return render(request, 'buyer/product-all.html', {'products': products, 'category_l1':category_l1, 'category_l2':category_l2})
    except:
        return render(request, 'error-404.html')

def product_detail(request, slug):
    category_l1 = Category.objects.all()[:6]    # first 6 categories in category_l1
    category_l2 = Category.objects.all()[6:]    # start from 6th index to end categories in category_l2
    wishlist_flag = False   # create a wishlist_flag boolean variable with default False Value.
    try:
        product = Product.objects.get(slug=slug)
        qty_range = [num for num in range(2,11)]
        productimage = ProductImages.objects.filter(product=product)
        try:
            user = User.objects.get(email=request.session['email'])
            Wishlist.objects.get(user=user, product=product)
            wishlist_flag=True
        except:
            pass
        return render(request, 'buyer/product-detail.html', {'qty_range':qty_range,'wishlist_flag':wishlist_flag,'product':product, 'productimage':productimage, 'category_l1':category_l1, 'category_l2':category_l2})
    except:
        return render(request, 'error-404.html')
        

''' End Buyer User Function '''