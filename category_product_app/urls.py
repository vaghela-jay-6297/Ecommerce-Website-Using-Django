from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Seller User Url
        # Category URL
    path('add-category/', views.add_category, name='add-category'), # add category
    path('del-up-category/', views.del_up_category, name="del-up-category"),    # View/Delete/Update action from Category table 
    path('drop-category/<slug:slug>', views.drop_category, name='drop-category'),  # delete/drop category
    path('update-category/<slug:slug>', views.update_category, name='update-category'),  # update/edit category
        # Product URL
    path('add-product/', views.add_product, name="add-product"),    # add product
    path('view-del-up-product/', views.view_del_up_product, name="view-del-up-product"),     # View/Delete/Update action from Product table
    path('view-product/<slug:slug>', views.view_product, name='view-product'),  # view single product
    path('update-product/<slug:slug>', views.update_product, name='update-product'),  # update product
    path('drop-product/<slug:slug>', views.drop_product, name='drop-product'),  # delete/drop product

    # Buyer User Url
    path('', views.category, name='category'),  # Show All Categorys
    path('product-all/', views.product_all, name='product-all'),    # show All Products
    path('product-by-category/<str:category_name>', views.product_by_category, name='product-by-category'),    # Filter Product By Category
    path('product-detail/<slug:slug>', views.product_detail, name='product-detail'),    # Show single product details
]

# here set media folder when user's uupload their images like product image, profile picture...,
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
