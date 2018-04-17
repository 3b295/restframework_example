from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import apis


urlpatterns = format_suffix_patterns([
    path('products/', apis.ProductList.as_view()),
    path('games/', apis.GameList.as_view()),
    path('games/<pk>/', apis.GameDetail.as_view()),
    path('books/', apis.BookList.as_view()),
    path('books/<pk>/', apis.BookDetail.as_view()),
    path('clothes/', apis.ClothingList.as_view()),
    path('clothes/<pk>/', apis.ClothingDetail.as_view()),
])