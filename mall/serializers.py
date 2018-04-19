from rest_framework import serializers
from decimal import Decimal
from . import models


class ClothingSerializer(serializers.Serializer):
    CATEGORY_CHOICE = (
        ('jeans', '牛仔裤'),
        ('shorts', '短裤'),
        ('Cotton_trousers', '棉裤'),
        ('Short_sleeve', '短袖'),
        ('coat', '外衣'),
        ('Sweater', '卫衣'),
        ('Shoes', '板鞋'),
        ('leather_shoes', '皮鞋'),
        ('sports_shoes', '运动鞋'),
    )

    name = serializers.CharField(max_length=100, required=True)
    price = serializers.DecimalField(max_digits=20, decimal_places=2, min_value=Decimal(.01), required=True)
    size = serializers.IntegerField(min_value=0, required=True)

    category = serializers.ChoiceField(CATEGORY_CHOICE)

    color = serializers.CharField(max_length=32, allow_blank=True)
    material = serializers.CharField(max_length=32, allow_blank=True)

    def create(self, validated_data):
        pro = models.ClothingModel.objects.create(price=validated_data['price'],
                                                  name=validated_data['name'],
                                                  size=validated_data['size'])
        models.CategoryModel.objects.create(product=pro, name=validated_data['category'])
        for name, value in validated_data.items():
            if name not in {'price', 'name', 'size', 'category'} and value:
                models.ClothingAttrModel.objects.create(product=pro, name=name, value=value)
        return pro

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.email)
        instance.price = validated_data.get('price', instance.content)
        return instance

    def to_representation(self, instance):
        return dict({x.name: x.value for x in instance.attrs.all()},
                    price=instance.price,
                    name=instance.name,
                    size=instance.size,
                    category=[x.name for x in instance.category.all()])


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
