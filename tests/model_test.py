from rest_framework.test import APITestCase
from mall.models import BaseProductModel, GameModel, CategoryModel


class ProductModelTester(APITestCase):
    def test_create_category(self):
        g = GameModel.objects.create(platform=GameModel.PS, name='test game', price=666)

        cate = []
        for i in CategoryModel.objects.filter(product=g):
            cate.append(i.name)

        self.assertListEqual(cate, ['all', 'game'])

    def test_base_product_attr(self):
        g = GameModel.objects.create(platform=GameModel.PS, name='test game', price=666)
        base = g.baseproductmodel_ptr
        self.assertJSONEqual(base.attr, {'platform': GameModel.PS})



