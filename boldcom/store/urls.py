from django.urls import path
from . import views 
    
    
urlpatterns = [
    path('', views.store, name="store"),
    # ===> This url wwill get the categories of each product
    path('category/<slug:category_slug>/', views.store, name="products_by_category"),
    # this will display the detail page of the product, which means about the products
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name="product_detail"),
    path('search/', views.search, name='search')
]