import unittest

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestAuthViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestAuthViews, cls).setUpClass()

        new_user = User.objects.create_user(
            username ="test_user",
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="secret"
        )

    def test_login(self):

        response = self.client.post(reverse("check_mate:login"), {"username": ["test_user"], "password": ["secret"]})

        self.assertEqual(response.status_code, 302)

        self.client.logout()

        bad_login = self.client.post(reverse("check_mate:login"), {"username": ["test_user"], "password": ["secrdset"]})

        self.assertIn('Login failed. Your username or password is incorrect.'.encode(), bad_login.content)

    def test_registration(self):

        response = self.client.post(reverse("check_mate:register"), {"username": "new_user", "first_name": "First", "last_name": "Name", "email": "test@test.com", "password": "password"})

        self.assertEqual(response.status_code, 302)