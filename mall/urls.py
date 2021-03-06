from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import apis


urlpatterns = format_suffix_patterns([
    path('products/', apis.ProductList.as_view(), name='product-list'),
    path('products/<pk>', apis.ProductDetail.as_view(), name='product-detail'),
    path('games/', apis.GameList.as_view()),
    path('games/<pk>/', apis.GameDetail.as_view(), name='game-detail'),
    path('books/', apis.BookList.as_view()),
    path('books/<pk>/', apis.BookDetail.as_view(), name='book-detail'),
    path('clothes/', apis.ClothingList.as_view()),
    path('clothes/<pk>/', apis.ClothingDetail.as_view(), name='clothing-detail'),
    path('shopping-cart/', apis.ShoppingCartList.as_view(), name='shopping-cart'),
    path('shopping-cart/<pk>/', apis.ShoppingCartDetail.as_view(), name='shopping-cart-detail'),
    path('orders/', apis.OrderList.as_view(), name='order-list'),
    path('orders/<pk>/', apis.OrderDetail.as_view(), name='order-detail'),
])