from django.contrib.admin import site
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import CharField

from . import models


site.register((models.GameModel, models.ClothingModel, models.BookModel))


class OrderMediaInline(admin.StackedInline):
    model = models.OrderMap


@admin.register(models.OrderModel)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderMediaInline]
    list_display = ['id', 'owner', 'address', 'phone_number', 'timestamp']


site.register(models.User, UserAdmin)  # FIX:自己添加的字段不在这个表单内
site.register(models.ShoppingCartModel)
site.register(models.CategoryModel)
site.register(models.CostModel)





