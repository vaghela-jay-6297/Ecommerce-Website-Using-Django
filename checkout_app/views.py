from django.shortcuts import render, redirect
from account.models import User # import models from account.models.py
from cart_wishlist_app.models import Cart, Wishlist, DiscountCoupon # import models from cart_wishlist_app.models.py
from category_product_app.models import Category, Product   # import models from category_product_app.models.py
from account.views import get_Catories  # import fun from account.views.py 
from .models import User_address
from django.conf import settings    # get all setting varable or function
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = 'http://localhost:8000/'

# Create your views here.
def discount_coupon(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session['email']:
            user = User.objects.get(email=request.session['email']) # get current logged in user object
            cart = Cart.objects.filter(user=user)   # get cart product object user-wise filter
            # check user's entered discount coupon
            if request.method == 'POST':
                try:
                    coupon = DiscountCoupon.objects.get(coupon_code=request.POST['discount-coupon'])
                    # subtract discount amount from total amount & update session variable.
                    request.session['total'] = request.session['total'] - float(coupon.discount_amount)
                    request.session['discount_code'] = coupon.coupon_code  # set coupon code in session
                    request.session['discount_amt'] = float(coupon.discount_amount)  # set discount amount in session
                    success = "You Get Rs. " + str(coupon.discount_amount) +  " Discount."  # success message
                    return render(request, 'buyer/checkout.html', {'cart':cart,'success':success, 'category_l1': category_l1, 'category_l2': category_l2})
                except:
                    warning = "Coupon Does not Exist."  # warning message
                    return render(request, 'buyer/checkout.html', {'cart':cart,'warning':warning,'category_l1': category_l1, 'category_l2': category_l2})
            else:
                try:
                    del request.session['discount_code']    # when user refresh this page then session will destroy 
                    del request.session['discount_amt'] # when user refresh this page then session will destroy 
                except:
                    pass
                return render(request, 'buyer/checkout.html',{'cart':cart,'category_l1': category_l1, 'category_l2': category_l2})  
    except:
        return render(request, 'error-404.html',{'category_l1': category_l1, 'category_l2': category_l2})

    
def checkout(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session['email']:
            user = User.objects.get(email=request.session['email'])
            cart = Cart.objects.filter(user=user)
            return render(request, 'buyer/checkout.html', {'cart':cart, 'user':user,'category_l1': category_l1, 'category_l2': category_l2})          
    except:
        return render(request, 'error-404.html',{'category_l1': category_l1, 'category_l2': category_l2})

def new_address(request):
    user=User.objects.get(email=request.session['email'])
    if request.method == 'POST':
       useraddress = User_address.objects.create(user=user,company_name=request.POST['company-name'], 
                            country=request.POST['country'], address_l1= request.POST['address1'], 
                            address_l2=request.POST['address2'], city= request.POST['city'], 
                            state=request.POST['state'], postcode=request.POST['postcode'], 
                            mobile=request.POST['mobile'], notes=request.POST['notes'])
       address = useraddress.address_l1 + ' ' + useraddress.city + ' ' + useraddress.state + ' ' +useraddress.postcode
       request.session['address'] = address
    return redirect('order-checkout-process')

def order_checkout_process(request):
    category_l1 , category_l2 = get_Catories()  # get all categories using custom fun get_Cateories
    try:
        if request.session['email']:
            user = User.objects.get(email=request.session['email'])
            cart = Cart.objects.filter(user=user)
            return render(request, 'buyer/checkout.html', {'cart':cart, 'user':user,'category_l1': category_l1, 'category_l2': category_l2})
    except Exception as e:
        print(e)
        return render(request, 'error-404.html',{'category_l1': category_l1, 'category_l2': category_l2})

@csrf_exempt
def stripe_checkout_session(request):
    try:
        amount = int(json.load(request)['amount'])
        final_amount = amount*100
        print("**********************", final_amount)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
		    line_items=[{
			    'price_data': {
				    'currency': 'inr',
				    'product_data': {
					    'name': 'Checkout Session Data',
					    },
				    'unit_amount': final_amount,
				    },
			    'quantity': 1,
			}],
		    mode='payment',
            success_url = DOMAIN + '/success.html',  # when payment is successful    
            cancel_url = DOMAIN + '/cancel.html',    # when payment is failed/cancelled
        )
    except Exception as e:
        return str(e)
    # return redirect(checkout_session.url, code=303)
    return JsonResponse({'id': session.id})

def pay_success(request):
    return render(request, 'buyer/success.html')

def pay_cancel(request):
    return render(request, 'buyer/cancel.html')

def order_detail(request):
    return render(request, 'buyer/order-detail.html')