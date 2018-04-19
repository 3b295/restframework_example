from rest_framework import filters
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F, FloatField

from . import models
from . import serializers
from . import paginations
from .filters import IsOwnerFilterBackend
from .permissions import IsOwner


class ProductList(generics.ListAPIView):
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filter_fields = ('category__name',)

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    pagination_class = paginations.StandardResultsSetPagination

    queryset = models.BaseProductModel.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    queryset = models.BaseProductModel.objects.all()
    serializer_class = serializers.ProductSerializer


class GameList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    pagination_class = paginations.StandardResultsSetPagination

    queryset = models.GameModel.objects.all()
    serializer_class = serializers.GameSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    queryset = models.GameModel.objects.all()
    serializer_class = serializers.GameSerializer


class ClothingList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filter_fields = ('category__name',)

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    pagination_class = paginations.StandardResultsSetPagination

    queryset = models.ClothingModel.objects.all()
    serializer_class = serializers.ClothingSerializer


class ClothingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    queryset = models.ClothingModel.objects.all()
    serializer_class = serializers.ClothingSerializer


class BookList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    queryset = models.BookModel.objects.all()
    serializer_class = serializers.BookSerializer
    pagination_class = paginations.StandardResultsSetPagination


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

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


class OrderList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (IsOwnerFilterBackend,)
    queryset = models.OrderModel.objects.all()
    serializer_class = serializers.OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = models.OrderModel.objects.create(owner=request.user,
                                                 address=serializer.data['address'],
                                                 phone_number=serializer.data['phone_number'],
                                                 )

        for item in models.ShoppingCartModel.objects.filter(owner=request.user):
            if item.is_active:
                models.OrderMap.objects.create(order=order,
                                               product=item.product,
                                               real_price=item.product.price,
                                               numbers=item.numbers)
                item.delete()
                print('1')
                from IPython import embed;embed()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderDetail(mixins.RetrieveModelMixin,
                  generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = models.OrderModel.objects.all()
    serializer_class = serializers.OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


