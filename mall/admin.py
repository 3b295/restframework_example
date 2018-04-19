from django.contrib.admin import site
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


site.register((models.GameModel, models.ClothingModel, models.BookModel))


class OrderMediaInline(admin.TabularInline):
    model = models.OrderMap
    extra = 0


@admin.register(models.OrderModel)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderMediaInline]
    list_display = ['id', 'owner', 'address', 'phone_number', 'timestamp', 'price', 'status']

    fields = ['status', 'price', 'address', 'phone_number']
    list_filter = ['owner']


site.register(models.User, UserAdmin)
site.register(models.ShoppingCartModel)
site.register(models.CategoryModel)
site.register(models.ClothingAttrModel)





