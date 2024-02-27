from django.shortcuts import render, redirect
from account.views import get_Catories  # in this fun get all categories from DB
from .models import Wishlist, Cart, DiscountCoupon    # get Wishlist, Cart model from models.py file of current folder 
from account.models import User # get User model from models.py file of account app folder 
from category_product_app.models import Category, Product   # get Category, Product model from models.py file of category_product_app folder
from django.utils.crypto import get_random_string   # generate slug value of product


# Create your views here.
''' Buyer User Function '''
def cart(request):  # buyer view their cart details.
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session["email"]:    # if user loggin session avilable
            user = User.objects.get(email=request.session['email']) # get current logged in user object
            cart = Cart.objects.filter(user=user)   # get cart product object user-wise filter
            request.session['cart_count'] = len(cart)   # update value of session variable bcz session already created when user login.
            sub_total = 0.0 # sub_total variable for add value 
            total = 0.0 # total variable is main total after subtract discount & add shipping
            for i in cart:  # fetch total price 
                sub_total = float(sub_total) + float(i.total_price) # calculate sub total
            
            # if sub total value is less 1500 than add shippin charge.
            if sub_total < 1500.0:    
                total = sub_total + 150.00  # 150 shipping charge
            else:
                total = sub_total   # free shipping
            
            request.session['sub_total'] = sub_total    # set sub total value into session variable.
            request.session['total'] = total    # set total value into session variable so you can access anywhere.
                
            return render(request, 'buyer/cart.html', {'cart':cart, 'category_l1': category_l1, 'category_l2': category_l2})
    except:
        return render(request, 'error-404.html',{'category_l1': category_l1, 'category_l2': category_l2})
    
def add_to_cart(request, product_slug):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session["email"]:    # if user loggin session avilable
            if request.method == 'POST':    # if Submit form request is POST
                user = User.objects.get(email=request.session['email']) # get current logged in user object
                product = Product.objects.get(slug=product_slug)    # get product where slug=product_slug
                slug = get_random_string(length=24) # generate 12 character unique slug for cart
                qty = int(request.POST['qty'])   # get qty from user side & convert into int
                size = request.POST['size'] # get size from user side
                
                # create cart object into DB
                Cart.objects.create(user=user, product=product, cart_slug=slug, 
                                    product_price=product.offer_price, total_price=product.offer_price*qty,
                                    qty=qty, product_size=size, payment_status=False) 
                return redirect('cart') # return redirect to wishlist
            else:
                pass
    except:
        return render(request, 'error-404.html', {'category_l1': category_l1, 'category_l2': category_l2})

def remove_from_cart(request, product_slug):
    pass


def wishlist(request):  # buyer view their wishlist details.
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session["email"]:    # if user loggin session avilable
            user = User.objects.get(email=request.session['email']) # get current logged in user object
            wishlist = Wishlist.objects.filter(user=user)   # get wishlist product object user-wise filter
            request.session['wishlist_count'] = len(wishlist)   # update value of session variable bcz session already created when user login.
            return render(request, 'buyer/wishlist.html', {'wishlist':wishlist,'category_l1': category_l1, 'category_l2': category_l2})    
    except:
        return render(request, 'error-404.html')
    
def add_to_wishlist(request, product_slug):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session["email"]:    # if user loggin session avilable
            user = User.objects.get(email=request.session['email']) # get current logged in user object
            product = Product.objects.get(slug=product_slug)    # get product where slug=product_slug
            Wishlist.objects.create(user=user, product=product) # create wishlist object
            return redirect('wishlist') # return redirect to wishlist
    except:
        return render(request, 'error-404.html', {'category_l1': category_l1, 'category_l2': category_l2})

def remove_from_wishlist(request, product_slug):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session["email"]:    # if user loggin session avilable
            user = User.objects.get(email=request.session['email']) # get current logged in user object
            product = Product.objects.get(slug=product_slug)    # get product where slug=product_slug
            wishlist=Wishlist.objects.get(user=user, product=product) # create wishlist object
            wishlist.delete()
            return redirect('wishlist') # return redirect to wishlist
    except:
        return render(request, 'error-404.html', {'category_l1': category_l1, 'category_l2': category_l2})

def new_address(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session["email"]:    # if user loggin session avilable
            user = User.objects.get(email=request.session['email']) # get current logged in user object
            if request.method == 'POST':    
                user = User_address.objects.create(user=user, company_name=request.POST['company-name'], 
                                            country=request.POST['country'], address_l1= request.POST['address1'], 
                                            address_l2=request.POST['address2'], city= request.POST['city'], 
                                            state=request.POST['state'], postcode=request.POST['postcode'], 
                                            mobile=request.POST['mobile'], notes=request.POST['notes'])
                return redirect('cart')
            else:
                return render(request, 'buyer/new-address.html', {'category_l1': category_l1, 'category_l2': category_l2})
            
    except:
        return render(request, 'error-404.html', {'category_l1': category_l1, 'category_l2': category_l2})

''' End Buyer User Function '''



''' Seller User Function '''
def add_coupon(request):    # seller can add discount coupon
    try:
        if request.session["email"]:    # if user loggin session avilable
            user = User.objects.get(email=request.session["email"]) # get current user object
            if request.method == 'POST':    # if Submit form request is POST
                try:
                    # try to get coupon code
                    DiscountCoupon.objects.get(coupon_code=request.POST['dis-code'])
                    warning = "Discount Code Already Exist."  # warning message
                    return render(request, 'seller/others/seller-add-coupon.html', {'warning':warning})
                except:
                    # add object into Discount_coupon table.
                    DiscountCoupon.objects.create(user=user,
                                                   coupon_code=request.POST['dis-code'],
                                                   discount_amount=request.POST['dis-price'])
                    success = "Discount Code Added."  # success message
                    return render(request, 'seller/others/seller-add-coupon.html', {'success':success}) 
            else:
                return render(request, 'seller/others/seller-add-coupon.html')
    except:
        return render(request, 'error-404.html')

def view_del_coupon(request):   # seller can view and delete their discount coupon code.
    try:
        if request.session["email"]:    # if user loggin session avilable
            user = User.objects.get(email=request.session["email"]) # get current user object
            coupon = DiscountCoupon.objects.filter(user=user)
            return render(request, 'seller/others/seller-view-del-coupon.html', {'coupon':coupon})
    except:
        return render(request, 'error-404.html')
    
def delete_coupon(request, pk): # seller can delete their discount coupon code.
    try:
        if request.session["email"]:    # if user loggin session avilable
            coupon = DiscountCoupon.objects.get(pk=pk)  # get coupon object 
            coupon.delete() # delete object
            return redirect('view-del-coupon')
    except:
        return render(request, 'error-404.html')
    
''' End Seller User Function '''