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


