from django.urls import path

from products import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/create-order/', views.create_order, name='create_order'),
]