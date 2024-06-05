from django.contrib import admin 
from django.urls import path, include 
from django.conf.urls.static import static

from store import views

urlpatterns = [
    path('', views.index, name='store_home'),
    path('shop', views.all_products, name='shop'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('search-by-image/', views.search_by_image, name='search_by_image'),
    
]