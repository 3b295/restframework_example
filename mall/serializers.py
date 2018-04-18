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
    attr = serializers.JSONField()

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


class OrderMapSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True)

    class Meta:
        model = models.OrderMap
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    id = serializers.HyperlinkedRelatedField(read_only=True, view_name='order-detail')
    ordermap_set = OrderMapSerializer(many=True, read_only=True)

    class Meta:
        model = models.OrderModel
        fields = ('id', 'ordermap_set', 'timestamp', 'address', 'phone_number', 'owner')


