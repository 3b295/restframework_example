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


class ShoppingCartGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShoppingCartMap
        fields = ('numbers', 'product')
        depth = 1


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    方便读
    """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    shoppingcartmap_set = ShoppingCartGoodSerializer(many=True, read_only=True)

    class Meta:
        model = models.ShoppingCartModel
        fields = ('shoppingcartmap_set', 'id', 'owner')


class ShoppingCartForChangeSerializer(serializers.ModelSerializer):
    """方便写"""
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goods = serializers.PrimaryKeyRelatedField(queryset=models.BaseProductModel.objects.all(), many=True)

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
