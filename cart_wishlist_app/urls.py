from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        # Cart URLs
    path('cart/', views.cart, name='cart'), # buyer view cart view
    path('add-to-cart/<slug:product_slug>', views.add_to_cart, name='add-to-cart'), # buyer add product to cart
    path('remove-from-cart/<slug:product_slug>', views.remove_from_cart, name='remove-from-cart'), # buyer add product to cart
    
    path('new-address/', views.new_address, name='new-address'), # add new shipping address 
    
        # Wishlist URLs
    path('wishlist/', views.wishlist, name='wishlist'), # buyer view wishlist view
    path('add-to-wishlist/<slug:product_slug>', views.add_to_wishlist, name='add-to-wishlist'), # buyer add product to wishlist
    path('remove-from-wishlist/<slug:product_slug>', views.remove_from_wishlist, name='remove-from-wishlist'), # buyer add product to wishlist
    
        # seller Discount Coupon
    path('add-coupon/', views.add_coupon, name='add-coupon'), # Seller Can add discount Coupon.
    path('view-del-coupon/', views.view_del_coupon, name='view-del-coupon'), # Seller Can view/delet discount Coupon.
    path('delete-coupon/<int:pk>', views.delete_coupon, name='delete-coupon'), # Seller Can delete discount Coupon.
]

# here set media folder when user's uupload their images like product image, profile picture...,
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)