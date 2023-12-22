from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Buyer User's URL
    path('', views.home, name='home'),
    path('newuser/', views.register, name='register'),  # user registration 
    path('login/', views.login, name='login'),  # user login
    path('logout/', views.logout, name='logout'),   # user logout
    path('change-password/', views.change_password, name='change-password'),    # user change password
    path('forgot-password/',views.forgot_password, name='forgot-password'), # user forgot password(Enter Email)
    path('otp-verifiction/', views.otp_verifiction, name='otp-verifiction'), # user email verify using otp session variable
    path('new-password/', views.new_password, name='new-password'), # user's enter new password when email is verifyed.
    path('user-profile/', views.user_profile, name='user-profile'), # user's profile updation
    path('product-gridview/', views.product_gridview, name='product-gridview'), # user grid View product 
    path('product-detail/<slug:slug>/', views.product_detail, name='product-detail'),  # user view single product details.
    path('product-listview/', views.product_listview, name='product-listview'), # user list View product
    path('blog/', views.blog, name='blog'), # user blog 
    path('contact-us/', views.contact_us, name='contact-us'),   # user contact us
    path('about-us/', views.about_us, name='about-us'), # user about us
    path('wishlist/', views.wishlist, name='wishlist'), # wishlist product details template
    path('add-to-wishlist/<slug:slug>', views.add_to_wishlist, name='add-to-wishlist'), # user add product to wishlist
    path('remove-from-wishlist/<slug:slug>', views.remove_from_wishlist, name='remove-from-wishlist'),  # user remove product from wishlist
    path('cart/', views.cart,name='cart'),  # user's cart template
    path('add-to-cart/<slug:slug>', views.add_to_cart, name='add-to-cart'), # user's add products into cart.
    path('remove-from-cart/<slug:slug>', views.remove_from_cart, name='remove-from-cart'), # user's remove products from cart.
    path('change-qty/<slug:slug>', views.change_qty, name='change-qty'),    # when user change product quntity at that time heat this url
    

    # Seller User's URLs
    path('seller-add-product/', views.seller_add_product, name='seller-add-product'),   # seller add their product
    path('seller-curd-product/', views.seller_curd_product, name='seller-curd-product'),    # seller view,update,delete their product
    path('seller-product-detail/<slug:slug>/', views.seller_product_detail, name='seller-product-detail'),  # seller view product details
    path('seller-delete-product/<slug:slug>/', views.seller_delete_product, name='seller-delete-product'),  # seller delete their product
]

# here set media folder when user's uupload their images like product image, profile picture...,
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)