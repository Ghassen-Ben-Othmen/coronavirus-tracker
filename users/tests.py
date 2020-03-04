from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token


# Create your tests here.

class TestAuth(TestCase):

    def setUp(self):
        self.client = Client()
        self.loginUrl = reverse('login-user')
        self.registerUrl = reverse('register-user')
        self.logoutUrl = reverse('logout-user')

        # register a user
        user = {
            "email": "g@gmail.com",
            "username": "ghassen",
            "password": "123"
        }
        response = self.client.post(self.registerUrl, user)
        self.token = response.json()['token']


    def test_register_valid_user(self):
        data = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123"
        }

        response = self.client.post(self.registerUrl, data=data)

        user = User.objects.filter(username=data['username']).get()

        # get token from db
        token = Token.objects.filter(user=user.id).get()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['token'], token.key)
        self.assertEqual(data['username'], user.username)

    def test_login_valid_user(self):
        data = {
            "username": "ghassen",
            "password": "123"
        }

        response = self.client.post(self.loginUrl, data=data)

        self.assertEquals(response.status_code, 200)


    def test_logout_user(self):

        count_token_before_logout = Token.objects.count()
        
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        response = self.client.post(self.logoutUrl, data=None, **headers)

        count_token_after_logout = Token.objects.count()


        self.assertEqual(count_token_before_logout - 1, count_token_after_logout)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['logout'], True)