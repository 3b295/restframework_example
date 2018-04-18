from rest_framework import serializers
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


class ShoppingCartReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShoppingCartModel
        fields = ('id', 'numbers', 'product', 'is_active')
        depth = 1


class ShoppingCartSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    numbers = serializers.IntegerField(default=1, min_value=1)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = models.ShoppingCartModel
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='order_map.price')

    class Meta:
        model = models.OrderModel
        fields = '__all__'
