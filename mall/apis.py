from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from . import models
from . import serializers


class ProductList(generics.ListAPIView):
    queryset = models.BaseProductModel.objects.all()
    serializer_class = serializers.ProductSerializer


class GameList(generics.ListCreateAPIView):
    queryset = models.GameModel.objects.all()
    serializer_class = serializers.GameSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = models.GameModel.objects.all()
    serializer_class = serializers.GameSerializer


class ClothingList(generics.ListCreateAPIView):
    queryset = models.ClothingModel.objects.all()
    serializer_class = serializers.ClothingSerializer


class ClothingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ClothingModel.objects.all()
    serializer_class = serializers.ClothingSerializer


class BookList(generics.ListCreateAPIView):
    queryset = models.BookModel.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BookModel.objects.all()
    serializer_class = serializers.BookSerializer

