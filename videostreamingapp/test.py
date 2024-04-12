# videostreamingapp/tests.py
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class UserAuthenticationTestCase(APITestCase):
    def test_user_signup(self):
        url = '/api/signup/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        url = '/api/login/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
