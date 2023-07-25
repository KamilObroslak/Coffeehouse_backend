from django.test import TestCase
from django.urls import reverse

from core.models import *
from faker import Faker
from django.contrib.auth.models import User


class UserRegisterTestCase(TestCase):
    def setUp(self):
        self.model = User.objects.create_user(username="usertest",
                                              email="test@test.com",
                                              password="test")
        print("UserRegisterTestCase setUp OK")

    def test_user_add(self):
        self.assertTrue(User.objects.all().exists())
        print("UserRegisterTestCase test_user_add OK")

    def test_user_modify(self):
        new_username = "my_new_nick"
        self.model.username = new_username
        self.model.save()
        print("UserRegisterTestCase test_user_modify OK")
        return new_username

    def test_user_delete(self):
        self.model.delete()
        self.assertFalse(User.objects.filter(username="my_new_nick").exists())
        print("UserRegisterTestCase test_user_delete OK")


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example_client", password="admin")
        print("UserLoginTestCase setUp - OK")

    def test_user_exists(self):
        self.assertTrue(User.objects.filter(username="example_client").exists())
        print("UserLoginTestCase test_user_exists OK")

    def test_user_modify(self):
        new_username = "my_new_nick"
        self.user.username = new_username
        self.user.save()
        self.assertEqual(self.user.username, new_username)
        print("UserLoginTestCase test_user_modify OK")

    def test_user_login(self):
        response = self.client.post('/core/login/', {'username': 'example_client', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)  # Sprawdzam, czy żądanie logowania zostało pomyślnie przetworzone.
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        print("UserLoginTestCase test_user_login OK")

    def test_user_delete(self):
        self.user.delete()
        self.assertFalse(User.objects.filter(username="example_client").exists())
        print("UserLoginTestCase test_user_delete OK")


# class UserLogoutTestCase(TestCase):
#
#     def test_user_login(self):
#         response = self.client.post('/core/login/', {'username': 'example_client', 'password': 'admin'})
#         self.assertEqual(response.status_code, 200)  # Sprawdzam, czy żądanie logowania zostało pomyślnie przetworzone.
#         self.assertTrue(response.wsgi_request.user.is_authenticated)
#         print("UserLoginTestCase test_user_login OK")
#
#     def test_user_logout(self):
#         response = self.client.post("/core/logout", {})
#         self.assertIn(response.status_code, [302, 301, 200]) # 302 to przekierowanie 200 OK
#         if response.status_code in [302, 301]:
#             self.assertRedirects(response, reverse("/core/login/"))
#         else:
#             self.assertTrue(response.wsgi_request.user.is_authenticated)
#         print("UserLogoutTestCase test_user_logout OK")
