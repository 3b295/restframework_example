from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient, APIClient
from mall import models


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


