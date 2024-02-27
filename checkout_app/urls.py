from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.checkout, name='checkout'), # Buyer can buy their product with inseting all details
    path('discount-coupon/', views.discount_coupon, name='discount_coupon'), # Buyer can add discount Coupon
    path('new-address/', views.new_address, name="new-address"),
    path('order-checkout-process/', views.order_checkout_process, name='order-checkout-process'), # order checkout process, payment, address
    
    # stripe
    path('stripe-checkout-session/', views.stripe_checkout_session, name="stripe-checkout-session"),    # create stripe session when user pay their payment
    path('pay-success/', views.pay_success, name='pay-success'),    # when user paid their payemnt sucessfully
    path('pay-cancel/', views.pay_cancel, name='pay-cancel'),   # when payment failed/cancelled
    
    # order
    path('order-detail/', views.order_detail, name='order-detail'), 
    
]

# here set media folder when user's uupload their images like product image, profile picture...,
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)