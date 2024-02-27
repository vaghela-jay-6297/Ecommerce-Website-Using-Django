from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password   # for create a pwwd and check pwd 
from .models import User   # get model from models.py file
from category_product_app.models import Category, Product   # get model from models.py file from category_product_app
from cart_wishlist_app.models import Wishlist, Cart   # get model from models.py file from cart_wishlist_app
import random   # generate random digits
from django.conf import settings    # get all setting varable or function
from django.core.mail import send_mail  # send mail to user
from django.utils.crypto import get_random_string   # generate slug value of product

# Create your views here.
def get_Catories():
    category_l1 = Category.objects.all()[:6]    # first 6 categories in category_l1
    category_l2 = Category.objects.all()[6:]    # start from 6th index to end categories in category_l2
    return category_l1, category_l2

def index(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    return render(request, 'index.html', {'category_l1': category_l1, 'category_l2': category_l2})    

def register(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session['email']:    # check user session email variable avilable or not? 
            return redirect('index')
    except:    # when session is not active.
        if request.method == 'POST':    # check html form request.
            try:    # here we check email & mobile is already registered or not. if registered then we never register again.
                User.objects.get(email=request.POST['register-email'])  # get the single user's details if email registered.   
                warning = "Email already Register."
                return render(request, 'index.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})    
            except:
                # check password & cpassword are same or not?
                if request.POST['register-password'] == request.POST['register-cpassword']:
                    # if passwords are same then we create a user in DB.
                    # make encrypt password using make_password func with password hasher 'sha1'
                    password = make_password(request.POST['register-password'], 'sha1')  
                    # create User
                    User.objects.create(user_type=request.POST['user_type'],
                                        email=request.POST['register-email'],
                                        fname=request.POST['fname'],
                                        lname=request.POST['lname'],
                                        mobile=request.POST['mobile'],
                                        password=password)
                    success = "Account Successfully Created for " + request.POST['fname']
                    return render(request, 'index.html', {'success': success, 'category_l1': category_l1, 'category_l2': category_l2})    
                else:
                    # passwords are not Matched!
                    warning = "Password and Confirm Password Does not Matched!"
                    return render(request, 'index.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})
        else:            
            return redirect('index')
    

def login(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session['email']:    # check user session email variable avilable or not? 
            return redirect('index')
    except:
        if request.method == 'POST':    # check login form method. if method is post then execute if block & method is get then execute else block.
            try:
                user=User.objects.get(email=request.POST['singin-email'])   # get single user object. when email is registered.
                # check_password is fun for checking the user's entered pwd & DB user hash pwd.(here password is users pwd, user.password is user's DB pwd hash key)
                if check_password(request.POST['singin-password'], user.password) :
                    request.session['user_type']=user.user_type # user_type session variable with current user's user_type value.
                    request.session['email']=user.email # email session variable with current user's email value.
                    request.session['fname']=user.fname # fname session variable with current user's fname value.
                    request.session['profile_picture']=user.profile_picture.url # profile_picture session variable with current user's profile_picture value.
                    
                    wishlist = Wishlist.objects.filter(user=user)   # get wishlist objects user-wise filter
                    request.session['wishlist_count'] = len(wishlist)   # get length of wishlist object assign to session variable.
                    
                    cart = Cart.objects.filter(user=user)   # get CArt objects user-wise filter
                    request.session['cart_count'] = len(cart)   # get length of Cart object assign to session variable.
                    sub_total=0.0   # inistialize variable
                    for price in cart:  # fetch price from cart object
                        sub_total = float(sub_total) + float(price.total_price) # calculate sub_total
                    request.session['sub_total'] = sub_total    # assign sub_total to sesion variable
                    
                    return render(request, 'index.html', {'category_l1': category_l1, 'category_l2': category_l2})
                
                else:   # when user password is Wrong.
                    warning = "Invalid User Password!"
                    return render(request, 'index.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})          
            
            except:
                # execute this block when user entered invalid credentials.
                warning = "Invalid User Credentials! Please Enter Valid Credentials."
                return render(request, 'index.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2}) 
        else:
            return redirect('index')
        
def logout(request):
    # automatically session is destroy within 5min if you not press any key or mouse click so that's why we use try and except block.
    try:
        del request.session['email']    # delete email session variable when user logout
        del request.session['user_type']    # delete user_type session variable when user logout
        del request.session['fname']    # delete fname session variable when user logout
        del request.session['profile_picture']    # delete profile_picture session variable when user logout
        del request.session['wishlist_count']   # delete wishlist_count session variable when user logout
        del request.session['cart_count']   # delete cart_count session variable when user logout
        del request.session['sub_total']    # delete sub_total session variable when user logout
        del request.session['total']    # delete total session variable when user logout
        # delete discount_code, discount_amt session variable when user logout & automatically destroy when order process will complete
        del request.session['discount_code']    
        del request.session['discount_amt'] 
        
        return redirect('index')
    except:
        warning = "User Session Timeout. please Login Again!"
        return render(request, 'index.html', {'warning': warning})        

def change_password(request):   # user can update their password
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    
    if request.method == "POST":    # if form method is POST then execute below block
        try:
            user = User.objects.get(email=request.session['email'])
            # compare new password & confirm password input
            if request.POST['new-password'] == request.POST['cnew-password']:
                if check_password(request.POST['old-password'], user.password): # compare old password & old user's DB password.
                    password = make_password(request.POST['new-password'], 'sha1')  # user password encryption
                    user.password = password    # user password updated
                    user.save()
                    return redirect('logout')
                else:
                    warning = "Invalid old Password!"
                    return render(request, 'account/change-password.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})    
            else:
                warning = "New Password and confirm New Password Does not Matched!"
                return render(request, 'account/change-password.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})
        except Exception as e:
            print("Exception: ", e)
    else:
        return render(request, 'account/change-password.html', {'category_l1': category_l1, 'category_l2': category_l2})

''' When user forgot their password'''
def forgot_password(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    if request.method == "POST":    # if form method is POST then execute below block 
        try:    # try to get user's entered email.
            user = User.objects.get(email=request.POST['forgot-email'])  # get user's enter email form DB.
            otp = random.randint(100000, 999999)    # genrate 6 digit random OTP
            
            subject = 'Forgot Password-OTP Verification'    # email subject.
            message = f'Hi {user.fname}, \n Your OTP is {otp}'  # email body
            email_from = settings.EMAIL_HOST_USER   # sender email get from settings.py file
            recipient_list = [user.email, ] # receiver]'s email 
            send_mail(subject, message, email_from, recipient_list )    # send_mail fun to send mail to receiver's email.
            
            # make otp session variable for otp varification, when otp verification complete than we delete otp session variable
            request.session['session_otp'] = otp    
            request.session['session_email'] = user.email
            success = "OTP Successfully Sent on your registered Email!"
            return render(request, 'account/otp-verification.html', {'success': success, 'category_l1': category_l1, 'category_l2': category_l2})    
        except: # when user's enteres email is not found
            warning = "Invalid Email Address! Please check!"
            return render(request, 'account/forgot-password.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})    
    else:
        return render(request, 'account/forgot-password.html')

''' Otp Based user verification '''
def otp_verification(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:    # trying to get session if session active otherwise found exception.
        request.session['session_email']    # get session value if active
        session_otp = str(request.session['session_otp'])    # get original otp by session varibale & convert to string
        if request.method == 'POST':    # if form method is POST then execute below block 
            user_otp = str(request.POST['user-otp']) # fetch user's entered OTP & convert into string
            if session_otp == user_otp: # compared user's OTP & original OTP
                del request.session['session_otp']  # when otp is verified then delete session
                return render(request, 'account/new-password.html', {'category_l1': category_l1, 'category_l2': category_l2})
            else:
                warning = "Invalid OTP! Please try Again!"
                return render(request, 'account/otp-verification.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})    
        else:
            return render(request, 'account/otp-verification.html', {'category_l1': category_l1, 'category_l2': category_l2})
    except:   # when session is not active
        return render(request, 'error-404.html', {'category_l1': category_l1, 'category_l2': category_l2})

''' User's can change their password when they are forgot. '''
def new_password(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:    # trying to get session if session active otherwise found exception.
        request.session['session_email']    # get session value if active
        if request.method == 'POST':    # if form method is POST then execute below block 
            if request.POST['new-password'] == request.POST['cnew-password']:    # compare new password & confirm password.
                try:
                    user = User.objects.get(email=request.session['session_email']) # fetch user object using session.
                    if check_password(request.POST['new-password'], user.password):  # compared user's entered password & DB password.
                        # if user's entered old password
                        warning = "You Enter Old Password! please Enter Different Password!"
                        return render(request, 'account/new-password.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})
                    else: # when user's entered old password
                        password = make_password(request.POST['new-password'], 'sha1')  # user password encryption
                        user.password = password    # update user password
                        user.save() # save user's data
                        del request.session['session_email']    # delete session variable because user's password is updated now.
                        success = user.fname + " Your Password Successfully Updated! please Login!"
                        return render(request, 'index.html', {'success': success, 'category_l1': category_l1, 'category_l2': category_l2})

                except:
                    pass
            else:
                warning = "New Password and confirm New Password Does not Matched!"
                return render(request, 'account/new-password.html', {'warning': warning, 'category_l1': category_l1, 'category_l2': category_l2})
        else:
            return render(request, 'account/new-password.html', {'category_l1': category_l1, 'category_l2': category_l2})
    except:   # when session is not active
        return render(request, 'error-404.html', {'category_l1': category_l1, 'category_l2': category_l2})

def blog(request):
    return render(request, 'blog.html')

def about_us(request):
    return render(request, 'about-us.html')

def contact_us(request):
    return render(request, 'contact-us.html')

def error_404(request):
    return render(request, 'error-404.html')