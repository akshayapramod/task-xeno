from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductList.as_view(), name='product_list_api'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail_api'),
    path('variants/', VariantList.as_view(), name='variant_list_api'),
    path('variants/<int:pk>/', VariantDetail.as_view(), name='variant_detail_api'),

]