from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

class TestData(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.dataUrl = reverse('data')

        # register user
        user = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123"
        }

        response = self.client.post(reverse('register-user'), data=user)
        self.token = response.json()['token']

    def test_get_data_without_authorization(self):
        response = self.client.get(self.dataUrl)

        self.assertEqual(response.status_code, 401)

    def test_get_data_with_authorization(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token '+self.token
        }
        response = self.client.get(self.dataUrl, **headers)

        self.assertEqual(response.status_code, 200)