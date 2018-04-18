import json

from decimal import Decimal
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    qq = models.CharField(max_length=20, blank=True, verbose_name='QQ')

    shoppingcart = models.ManyToManyField('BaseProductModel', through='ShoppingCartModel', related_name='owner')

    class Meta(AbstractUser.Meta):
        pass


class BaseProductModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    attr = models.TextField(editable=False)

    def __str__(self):
        return self.name

    def create_category(self):
        CategoryModel.objects.create(name='all', product=self)

    def save(self, *args, **kwargs):
        raw = {}
        for key, value in self.__dict__.items():
            if key not in {'_state', 'id', 'name', 'price', 'attr'} and not key.endswith('_id'):
                raw[key] = value
        self.attr = json.dumps(raw)

        super().save(*args, **kwargs)
        self.create_category()


class GameModel(BaseProductModel):
    PS = 'ps4'
    Switch = 'switch'
    Xbox = 'xbox'

    PLATFORM_CHOICE = (
        (Switch, 'Switch'),
        (PS, 'Play Station 4'),
        (Xbox, 'Xbox'),
    )

    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICE, blank=False, null=False)

    def create_category(self):
        super().create_category()
        CategoryModel.objects.create(name='game', product=self)


class ClothingModel(BaseProductModel):
    size = models.PositiveIntegerField()

    def create_category(self):
        super().create_category()
        CategoryModel.objects.create(name='clothing', product=self)


class CostModel(ClothingModel):
    color = models.CharField(max_length=255)

    def create_category(self):
        super().create_category()
        CategoryModel.objects.create(name='cost', product=self)


class BookModel(BaseProductModel):
    publisher = models.CharField(max_length=255)

    def create_category(self):
        super().create_category()
        CategoryModel.objects.create(name='book', product=self)


class CategoryModel(models.Model):
    name = models.CharField(max_length=255, blank=False)
    product = models.ForeignKey('BaseProductModel', on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return '{} -> {}'.format(self.product.name, self.name)


class OrderModel(models.Model):
    owner = models.ForeignKey('User', on_delete=models.Case)

    products = models.ManyToManyField(BaseProductModel, through='OrderMap')

    timestamp = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?\d\d+$', message=r"电话号码必须满足 ^\+?\d\d+$ 规则.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=20)

    def __str__(self):
        return self.owner.username

    class Meta:
        ordering = ('timestamp',)


class OrderMap(models.Model):
    order = models.ForeignKey('OrderModel', on_delete=models.CASCADE)
    product = models.ForeignKey('BaseProductModel', on_delete=models.CASCADE)

    real_price = models.DecimalField(max_digits=20, decimal_places=2, blank=False)
    numbers = models.PositiveIntegerField(default=1, blank=False)


class ShoppingCartModel(models.Model):
    """
    用户 和 商品 多对多的表
    """
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('BaseProductModel', on_delete=models.CASCADE)

    numbers = models.PositiveIntegerField(default=1, blank=False)
    is_active = models.BooleanField(default=True, blank=False)

    class Meta:
        unique_together = ('owner', 'product')

    def __str__(self):
        return "{}'s {}".format(self.owner.username, self.product.name)




