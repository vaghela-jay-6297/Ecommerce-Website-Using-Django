from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'), # user(seller, buyer) index
    path('register/',views.register, name='register'),  # user(seller, buyer) registration
    path('login/',views.login, name='login'),   # user(seller, buyer) login    
    path('logout/',views.logout, name='logout'),    # user(seller, buyer) logout
    path('change-password/',views.change_password, name='change-password'),    # user(seller, buyer) change password
    
    # forgot password URLs
    path('forgot-password/',views.forgot_password, name='forgot-password'),    # user(seller, buyer) Forgot password
    path('otp-verification/',views.otp_verification, name='otp-verification'),    # user(seller, buyer) OTP verification
    path('new-password/',views.new_password, name='new-password'),    # user(seller, buyer) New Password
    
    path('blog/', views.blog, name='blog'),
    path('about-us/',views.about_us, name='about-us'),
    path('contact-us/',views.contact_us, name='contact-us'),
    path('error-404/',views.error_404, name='error-404'),   # user(seller, buyer) Error page
]

# here set media folder when user's uupload their images like product image, profile picture...,
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
