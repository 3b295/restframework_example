from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    fixtures = ['test_data.json']

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


