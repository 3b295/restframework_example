from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F, FloatField

from . import models
from . import serializers
from .filters import IsOwnerFilterBackend
from .permissions import IsOwner


class ProductList(generics.ListAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    queryset = models.BaseProductModel.objects.all()
    serializer_class = serializers.ProductSerializer


class GameList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    queryset = models.GameModel.objects.all()
    serializer_class = serializers.GameSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = models.GameModel.objects.all()
    serializer_class = serializers.GameSerializer


class ClothingList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    queryset = models.ClothingModel.objects.all()
    serializer_class = serializers.ClothingSerializer


class ClothingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ClothingModel.objects.all()
    serializer_class = serializers.ClothingSerializer


class BookList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filter_fields = ('name', 'id', 'price')

    queryset = models.BookModel.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BookModel.objects.all()
    serializer_class = serializers.BookSerializer


class ShoppingCartList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.ShoppingCartModel.objects.all()
    serializer_class = serializers.ShoppingCartSerializer
    filter_backends = (IsOwnerFilterBackend,)

    def list(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = serializers.ShoppingCartReadOnlySerializer(queryset, many=True)
            return Response({'total price': queryset.aggregate(price=Sum(F('product__price') * F('numbers'),
                                                                         output_field=FloatField()))['price'],
                             'result': serializer.data})
        else:
            return super().list(request, *args, **kwargs)


class ShoppingCartDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = models.ShoppingCartModel.objects.all()
    serializer_class = serializers.ShoppingCartSerializer
