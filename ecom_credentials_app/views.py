from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password   # for create a pwwd and check pwd 
from .models import User, Product, Wishlist, Cart   # get model from models.py file
import random   # generate random digits
from django.conf import settings    # get all setting varable or function
from django.core.mail import send_mail  # send mail to user
from django.utils.crypto import get_random_string   # generate slug value of product

# Create your views here.
def home(request):
    try:
        user = User.objects.get(email=request.session['email'])
        if user.user_type == 'Buyer':   # if user type is buyer then oepn buyers pages
            return render(request, 'home.html')
        else:   # user is seller then open seller pages.
            return render(request, 'seller/seller-home.html')
    except:
        return render(request, 'home.html')
    
def register(request):
    if request.method == 'POST': # check html form request.
        try:    # here we check email & mobile is already registered or not. if registered then we never register again.
            User.objects.get(email=request.POST['email'])  # get the single user's details if email registered.   
            warning = "Email already Register."
            return render(request, 'register.html', {'warning': warning})    
        except:
            if request.POST['password'] == request.POST['cpassword']:   # check password & cpassword are same or not?
                # if passwords are same then we create a user in DB.
                # make encrypt password using make_password func with password hasher 'sha1'
                password = make_password(request.POST['password'], 'sha1')  
                # create User
                User.objects.create(user_type=request.POST['user_type'],
                                    fname=request.POST['fname'],
                                    lname=request.POST['lname'],
                                    email=request.POST['email'],
                                    mobile=request.POST['mobile'],
                                    address=request.POST['address'],
                                    profile_picture=request.FILES['profile_picture'],
                                    password=password)
                success = "Account Successfully Created for " + request.POST['fname']
                return render(request, 'login.html', {'success': success})    
            else:
                # passwords are not Matched!
                warning = "Password & Confirm Password Does not Matched!"
                return render(request, 'register.html', {'warning': warning})    
    else:
        # execute this block when form request is get.
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':    # check login form method. if method is post then execute if block & method is get then execute else block.
        try:
            user = User.objects.get(email=request.POST['email'])    # get single user object. when email is registered.
            # check_password is fun for checking the user's entered pwd & DB user hash pwd.(here password is users pwd, user.password is user's DB pwd hash key)
            if check_password(request.POST['password'], user.password):
                if user.user_type == 'Buyer':   # if user is buyer then open buyer page.
                    # if password are matched, we create a session
                    request.session['email']=user.email # email session variable with current user's email value.
                    request.session['fname']=user.fname # fname session variable with current user's fname value.
                    request.session['profile_picture']=user.profile_picture.url # profile_picture session variable with current user's profile_picture value.
                    wishlist = Wishlist.objects.filter(user=user)   # get wishlist product object user-wise filter
                    # wishlist_count contain count of wishlist product in session variable so we are access ant where after login.
                    request.session['wishlist_count'] = len(wishlist) 

                    cart = Cart.objects.filter(user=user)   # get cart product object user-wise filter 
                    # cart_count contain count of cart product in session variable so we are access ant where after login.
                    request.session['cart_count'] = len(cart) 
                    return render(request, 'home.html')
                else:   # user is seller then open seller home page.
                    request.session['email']=user.email # email session variable with current user's email value.
                    request.session['fname']=user.fname # fname session variable with current user's fname value.
                    request.session['profile_picture']=user.profile_picture.url # profile_picture session variable with current user's profile_picture value.
                    return render(request, 'seller/seller-home.html')
            else:
                warning = "Invalid User Password!"
                return render(request, 'login.html', {'warning': warning})          
        except:
            # execute this block when user entered invalid credentials.
            warning = "Invalid User Credentials! Please Enter Valid Credentials."
            return render(request, 'login.html', {'warning': warning})    
    else:
        # execute this block when form request is get.
        return render(request, 'login.html')

def logout(request):
    # automatically session is destroy within 5min if you not press any key or mouse click so that's why we use try and except block.
    try:
        del request.session['email']    # delete email session variable when user logout
        del request.session['fname']    # delete fname session variable when user logout
        del request.session['profile_picture']    # delete profile_picture  session variable when user logout
        del request.session['wishlist_count']   # delete wishlist_count  session variable when user logout
        del request.session['cart_count']   # delete cart_count  session variable when user logout
        return render(request, 'home.html')
    except:
        warning = "User Session Timeout. please Login Again!"
        return render(request, 'login.html', {'warning': warning})    

# When user Forgot their password.
def forgot_password(request):
    if request.method == 'POST':
        # execute this block when form request is POST.
        try:
            # get user's entered email object.
            user = User.objects.get(email=request.POST['femail'])    # get user's enter email object
            otp = random.randint(100000, 999999) # geerate 6 digit random OTP
            
            subject = 'Forgot Password-OTP Verification'    # email subject.
            message = f'Hi {user.fname}, \n Your OTP is {otp}'  # email body
            email_from = settings.EMAIL_HOST_USER   # sender email get from settings.py file
            recipient_list = [user.email, ] # receiver]'s email 
            send_mail(subject, message, email_from, recipient_list )    # send_mail fun to send mail to receiver's email.
            
            # make otp session variable for otp varification, when otp verification complete than we delete otp session variable
            request.session['forgot_pwd_otp'] = otp    
            request.session['forgot_pwd_email'] = user.email
            success = "OTP Successfully Sent on your registered Email!"
            return render(request, 'otp-verification.html', {'success': success})  
        except:
            # execute this block when user entered wrong email or unregistered email.
            warning = "Email Does not Exists!"
            return render(request, 'forgot-password.html', {'warning': warning})
    else:
        # execute this block when form request is get.
        return render(request, 'forgot-password.html')

# user's entered email varification process using otp.
def otp_verifiction(request):
    if request.method == 'POST':
        # execute this block when form request is POST.
        user_otp = str(request.POST['uotp']) # convert into str 
        otp = str(request.session['forgot_pwd_otp'])   # convert into str 
        
        if otp == user_otp:
            # execute this block when user's entered otp & session variable otp are same.
            # destroy session varibale bcoz forgot_pwd_otp is verified but forgot_pwd_email is not details we have to update user password using email session variable
            del request.session['forgot_pwd_otp']  
            return render(request, 'new-password.html')
        else:
            # execute this block when user entered wrong otp
            warning = "Invalid OTP"
            return render(request, 'otp-verification.html', {'warning': warning})
    else:
        # execute this block when form request is get.
        return render(request, 'otp-verification.html')

# whne email is veified user enter their new password.
def new_password(request):
    if request.method == 'POST':
        # execute this block when form request is POST.
        user = User.objects.get(email=request.session['forgot_pwd_email'])  # get user object.
        password = request.POST['new-password']
        cpassword = request.POST['new-password']
        # compare new password & confirm password input
        if password == cpassword:
            if check_password(password, user.password):   # check user's entered password is old or not?
                warning = "You Enter Old Password! please Enter Different Password!"
                return render(request, 'new-password.html', {'warning': warning})  
            else:   # when user enter different password compare to old password.
                try:
                    user.password = make_password(request.POST['new-password'], 'sha1') # user password encryption & update existing password
                    user.save() # save password into DB.
                    del request.session['forgot_pwd_email'] # delete session variable
                    success = "Password Successfully Updated! please Login!"
                    return render(request, 'login.html', {'success': success})   
                except:
                    pass
        else:
            # execute this block when new password & confirm new password does not matched.
            warning = "New Password & Confirm Password Does not Matched!"
            return render(request, 'new-password.html', {'warning': warning})   
        
    else:
         # execute this block when form request is get.
        return render(request, 'new-password.html')

def change_password(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.session['email']) # get current user object.
        # compare new password & confirm password input
        if request.POST['new-password'] == request.POST['cnew-password']:   
            # compare old password & old user's DB password.
            if check_password(request.POST['old-password'], user.password):
                password = make_password(request.POST['new-password'], 'sha1')  # user password encryption
                user.password = password    # insert encrypted password into db
                user.save() # save password into db
                success = "Password Successfully Updated!"
                return redirect('logout')
            else:
                # execute this block when user's enter wrong old password.
                warning = "Old Password Does not Matched!"
                return render(request, 'change-password.html', {'warning': warning})   
        else:
            # execute this block when new password & confirm new password does not matched.
            warning = "New Password & Confirm Password Does not Matched!"
            return render(request, 'change-password.html', {'warning': warning})   
    else:
        # execute this block when form request is get.
        return render(request, 'change-password.html')

def user_profile(request):
    # here update or delete user profile
    user = User.objects.get(email=request.session['email']) # fetch current user details
    if request.method == 'POST':    # check request form method 
        user.fname = request.POST['fname']  # update fname 
        user.lname = request.POST['lname']  # update lname
        user.mobile = request.POST['mobile']    # update mobile
        user.address = request.POST['address']  # update address
        try:
            user.profile_picture = request.FILES['profile_picture'] # update profile image
        except:
            pass
        user.save() # save change to save data into DB if you don't type this line, data won't save into DB.
        request.session['fname']=user.fname # now session value is change so update session variable with value
        request.session['profile_picture']=user.profile_picture.url # now session value is change so update session variable with value
        success = "Account Successfully Updated for " + request.POST['fname']   # success message
        return render(request, 'user-profile.html', {'user':user, 'success':success})   
    else:
        return render(request, 'user-profile.html', {'user':user})

def product_gridview(request):
    cart_flag = False   # create a cart_flag boolean variable with default False Value.
    user = User.objects.get(email=request.session['email']) # get current logged in user object
    product = Product.objects.all() # get all products
    try:
        # when product is already added in cart DB then we pass cart_flag is True otherwise False.
        Cart.objects.get(user=user, product=product)    
        cart_flag = True    # to change the ancher tag add to cart to remove from cart.
        print("*****************************",cart_flag)
    except:
        pass
    return render(request, 'product-gridview.html',{'product':product, 'cart_flag':cart_flag})

def product_listview(request):
    return render(request, 'product-listview.html')

def product_detail(request, slug):
    wishlist_flag = False   # create a wishlist_flag boolean variable with default False Value.
    cart_flag = False   # create a cart_flag boolean variable with default False Value.
    user = User.objects.get(email=request.session['email']) # get current logged in user object
    product = Product.objects.get(product_slug=slug)    # fetch product details where slug value is fetched slug value of url.    
    try:
        # when product is already added in wishlist DB then we pass wishlist_flag is True otherwise False.
        Wishlist.objects.get(user=user, product=product)    
        wishlist_flag = True    # to change the ancher tag add to wishlist to remove from wishlist.
    except:
        pass

    try:
        # when product is already added in cart DB then we pass cart_flag is True otherwise False.
        Cart.objects.get(user=user, product=product)    
        cart_flag = True    # to change the ancher tag add to cart to remove from cart.
    except:
        pass
    return render(request, 'product-detail.html', {'product':product, 'wishlist_flag':wishlist_flag, 'cart_flag':cart_flag})

def blog(request):
    return render(request, 'blog.html')

def contact_us(request):
    return render(request, 'contact-us.html')

def about_us(request):
    return render(request, 'about-us.html')

def add_to_wishlist(request, slug): # add product to wishlist
    user=User.objects.get(email=request.session['email'])   # get current logged in user object
    product=Product.objects.get(product_slug=slug)  # get product by unique slug value
    Wishlist.objects.create(user=user, product=product)  # create object using user & product foreignkey
    return redirect('wishlist') # redirect to wishlist url name.

def remove_from_wishlist(request, slug):
    user=User.objects.get(email=request.session['email'])   # get current logged in user object
    product=Product.objects.get(product_slug=slug)  # get product by unique slug value
    wishlist=Wishlist.objects.get(user=user, product=product)    # get wishlist object with same user & same product slug
    wishlist.delete()   # delete product object from DB
    return redirect('wishlist') # redirect to wishlist url name.

def wishlist(request):
    user = User.objects.get(email=request.session['email']) # get current logged in user object
    wishlist = Wishlist.objects.filter(user=user)   # get product object user-wise filter
    request.session['wishlist_count']=len(wishlist) # update value of session variable
    if len(wishlist) == 0:  # check wishlist is empty or not
        warning = "No Products in Wishlist."
        return render(request, 'wishlist.html',{'warning':warning})
    else:
        return render(request, 'wishlist.html', {'wishlist':wishlist})

def add_to_cart(request, slug):
    user = User.objects.get(email=request.session['email']) # get current logged in user object
    product = Product.objects.get(product_slug=slug)    # get product by unique slug value
    slug = get_random_string(length=24) # generate 12 character unique slug for cart
    Cart.objects.create(user=user, product=product, cart_slug=slug, product_price=product.product_price,
                        qty=1, total_price=product.product_price, payment_status=False) # create cart object into DB
    return redirect('cart') # return redirect to cart url

def remove_from_cart(request,slug):
    user = User.objects.get(email=request.session['email']) # get current logged in user object
    product = Product.objects.get(product_slug=slug)    # get product object by unique slug value
    cart = Cart.objects.get(user=user, product=product) # get cart object with condition where user=user & product=product
    cart.delete()   # delete that cart object
    return redirect('cart') # return redirect to cart url

def cart(request):
    user = User.objects.get(email=request.session['email']) # get current logged in user object
    cart = Cart.objects.filter(user=user)   # get cart object user-wise filter
    request.session['cart_count'] = len(cart)   # create cart_count session and we put value of length of cart object
    if len(cart) == 0:  # here we check length of cart is 0 then excute below if block
        warning = "No Products in Cart."    # message
        return render(request, 'wishlist.html',{'warning':warning})
    else:
        return render(request, 'cart.html', {'cart':cart})

def change_qty(request, slug):
    print("**************************************Submit ********************")
    cart = Cart.objects.get(cart_slug=slug) # get cart object by unique slug value
    product_qty = int(request.POST['qty'])  # get qty from user's form
    cart.total_price = cart.product_price * product_qty # update cart total_price
    cart.save() # save inserted data of cart into DB
    return redirect('cart') # return redirect to cart url



# Seller views
def seller_add_product(request):
    seller = User.objects.get(email=request.session['email'])
    if request.method == 'POST':    # check request form method
        slug = get_random_string(length=12) # generate 12 character unique slug
        # create product into db.
        Product.objects.create(user=seller,
                               product_category = request.POST['product_category'],
                               product_brand = request.POST['product_brand'],
                               product_size = request.POST['product_size'],
                               product_name = request.POST['product_name'],
                               product_desc = request.POST['product_desc'],
                               product_slug = slug,
                               product_image = request.FILES['product_image'],
                               product_price = request.POST['product_price']
        )
        success = "Product Successfully Added!"  # success message
        return render(request, 'seller/seller-add-product.html', {'success':success})   
    else:
        return render(request, 'seller/seller-add-product.html')

def seller_curd_product(request):
    try:
        seller=User.objects.get(email=request.session['email']) # fetch seller user by their login session email variable.
        product = Product.objects.filter(user=seller)   # fetch product only logging seller user not other session products.
        return render(request, 'seller/seller-curd-product.html', {'product':product})
    except:
        pass

def seller_product_detail(request, slug):
    # here fetch slug value from url and pass that value for getting product details from db
    try:
        product = Product.objects.get(product_slug=slug)    # fetch product details where slug value is fetched slug value of url.
        return render(request, 'seller/seller-product-detail.html',{'product':product})
    except:
        pass
    
def seller_delete_product(request, slug):
    try:
        product=Product.objects.get(product_slug=slug)  # get product where slug value is fetched slug value of url.
        product.delete()   # delete product
        return redirect('seller-curd-product')
    except:
        pass