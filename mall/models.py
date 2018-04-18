from decimal import Decimal
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    qq = models.CharField(max_length=20, blank=True, verbose_name='QQ')

    class Meta(AbstractUser.Meta):
        pass


class BaseProductModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return self.name


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


class ClothingModel(BaseProductModel):
    size = models.PositiveIntegerField()


class BookModel(BaseProductModel):
    publisher = models.CharField(max_length=255)


class OrderModel(models.Model):
    buyer = models.ForeignKey('User', on_delete=models.Case)
    goods = models.ManyToManyField(BaseProductModel, through='OrderMap')
    timestamp = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255, blank=False)

    phone_regex = RegexValidator(regex=r'^\+?\d\d+$',
                                 message=r"电话号码必须满足 ^\+?\d\d+$ 规则.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=20)

    def __str__(self):
        return self.buyer.username

    class Meta:
        ordering = ('timestamp',)


class OrderMap(models.Model):
    """多对多表"""
    order = models.ForeignKey('OrderModel', on_delete=models.CASCADE)
    product = models.ForeignKey('BaseProductModel', on_delete=models.CASCADE)

    real_price = models.DecimalField(max_digits=20, decimal_places=2, blank=False)
    numbers = models.PositiveIntegerField(default=1, blank=False)


class ShoppingCartMap(models.Model):
    shopping_cart = models.ForeignKey('ShoppingCartModel', on_delete=models.CASCADE)
    product = models.ForeignKey('BaseProductModel', on_delete=models.CASCADE)

    numbers = models.PositiveIntegerField(default=1, blank=False)


class ShoppingCartModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ManyToManyField(BaseProductModel, through='ShoppingCartMap', related_name='shopping_cart')

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}'s Shopping".format(self.owner.username)





