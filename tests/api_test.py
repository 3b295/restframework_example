import random
import string

from urllib.parse import urljoin
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from mall import models
from django.contrib.auth.hashers import make_password


class AccountTests(APITestCase):
    def test_create_account(self):
        pass


class ProductTest(APITestCase):
    fixtures = ['product.json']

    def test_pagination(self):
        path = '/products/'
        response = self.client.get(path)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)

    def test_permission_not_login(self):
        paths = [
            '/products/',
            '/games/',
            '/clothes/',
            '/books/',
        ]

        client = APIClient(enforce_csrf_checks=True)
        for path in paths:
            resp = client.get(path)
            self.assertEqual(status.HTTP_200_OK, resp.status_code)

            resp = client.post(path, json={'name': 'test', 'price': 10})
            self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)

    def test_permission_without_model_permission(self):
        username = '3b295'                  # 无模型权限
        password = 'XWYa314159'
        paths = [
            '/products/',
            '/games/',
            '/clothes/',
            '/books/',
        ]

        self.client.login(username=username, password=password)
        for path in paths:
            resp = self.client.get(path)
            self.assertEqual(status.HTTP_200_OK, resp.status_code)

            resp = self.client.post(path)
            self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)
            self.assertDictEqual(resp.data, {"detail": "您没有执行该操作的权限。"})

    def test_permission_with_model_permission(self):
        username = 'admin'              # 有模型权限
        password = 'XWYa314159'
        path = '/games/'

        self.client.login(username=username, password=password)
        resp = self.client.get(path)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        name = 'test'
        price = 110
        platform = models.GameModel.PS

        resp = self.client.post(path, data=dict(name=name, price=price, platform=platform))

        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        self.assertEqual(resp.data['name'], name)
        self.assertEqual(float(resp.data['price']), float(price))
        self.assertEqual(resp.data['platform'], platform)


class BlankUserMixin:
    def setUp(self):
        self.username = '09239)(*()#'
        self.password = '0920()34hj)(oisdf'
        self.user = models.User.objects.create(username=self.username, password=make_password(self.password))

    def login(self):
        self.client.login(username=self.username, password=self.password)


class ShoppingCartTester(BlankUserMixin, APITestCase):

    def test_get(self):
        path = '/shopping-cart/'

        self.login()

        resp = self.client.get(path)

        self.assertDictEqual(resp.data, {"total price": None, "result": []})

    def test_add(self):
        path = '/shopping-cart/'

        self.login()

        ps = []
        for i in range(10):
            name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            ps.append(models.BaseProductModel.objects.create(name=name, price=i+1))

        resp = self.client.post(path, data={'product': ps[0].id, 'numbers': 1})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        for i in range(1, 10):
            self.client.post(path, data={'product': ps[i].id, 'numbers': i+1})

        resp = self.client.get(path)
        self.assertEqual(resp.data['total price'], 385.0)

    def test_is_active(self):
        path = '/shopping-cart/'

        self.login()
        p = models.BaseProductModel.objects.create(name='test', price=1)

        self.client.post(path, data={'product': p.id, 'numbers': 1})

        resp = self.client.get(path)
        self.assertEqual(resp.data['total price'], 1.0)

        resp = self.client.put(path + str(p.id) + '/', data={'numbers': 1, 'is_active': False})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(path)
        self.assertEqual(resp.data['total price'], None)


class OrderTester(BlankUserMixin, APITestCase):

    def test_commit_null(self):
        path = '/orders/'
        self.login()
        resp = self.client.post(path, data={'address': 'test', 'numbers': '21324234'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_commit_success(self):
        path = '/orders/'
        shop_path = '/shopping-cart/'
        self.login()

        name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        p = models.BaseProductModel.objects.create(name=name, price=1)
        self.client.post(shop_path, data={'product': p.id, 'numbers': 1})

        resp = self.client.post(path, data={'address': 'test', 'phone_number': '21324234'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_delete_shopping_cart_before_commit(self):
        path = '/orders/'
        shop_path = '/shopping-cart/'
        self.login()

        name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        p = models.BaseProductModel.objects.create(name=name, price=1)
        self.client.post(shop_path, data={'product': p.id, 'numbers': 1})
        self.client.post(path, data={'address': 'test', 'phone_number': '21324234'})
        resp = self.client.get(shop_path)
        self.assertEqual(resp.data['total price'], None)







