from rest_framework import serializers
from django.db.models import Sum, Q
from . import models


class ClothingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClothingModel
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookModel
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GameModel
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseProductModel
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = models.ShoppingCartModel
        fields = ('id', 'product_num', 'name', 'owner', 'price', 'product')
