from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializers
from .filters import IsOwnerFilterBackend
from .permissions import IsOwner


class ProductList(generics.ListAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )

    queryset = models.BaseProductModel.objects.all()
    serializer_class = serializers.ProductSerializer


class GameList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )

    queryset = models.GameModel.objects.all()
    serializer_class = serializers.GameSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = models.GameModel.objects.all()
    serializer_class = serializers.GameSerializer


class ClothingList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )

    queryset = models.ClothingModel.objects.all()
    serializer_class = serializers.ClothingSerializer


class ClothingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ClothingModel.objects.all()
    serializer_class = serializers.ClothingSerializer


class BookList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name', )
    filter_fields = ('name', 'id', 'price')

    queryset = models.BookModel.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BookModel.objects.all()
    serializer_class = serializers.BookSerializer


class ShoppingCartDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = serializers.ShoppingCartSerializer
    queryset = models.ShoppingCartModel.objects.all()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('PUT', 'PATCH'):
            serializer_class = serializers.ShoppingCartForChangeSerializer
        if self.request.method == 'GET':
            serializer_class = serializers.ShoppingCartSerializer
        return serializer_class




