from django.test import TestCase
from core.models import *
from faker import Faker
from django.contrib.auth.models import User

#
# class UserRegisterTestCase(TestCase):
#     def setUpTestData(self):
#         self.model = User.objects.create_user(username="usertest",
#                                               email="test@test.com",
#                                               password="test")
#
#     def test_user_add(self):
#         self.assertTrue(User.objects.all().exists())
#
#     def test_user_modify(self):
#         new_username = "my_new_nick"
#         self.model.username = new_username
#         self.model.save()
#         return new_username
#
#     def test_user_delete(self):
#         self.model.delete()
#         self.assertFalse(User.objects.filter(username="my_new_nick").exists())


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example_client", password="admin")

    def test_user_exists(self):
        self.assertTrue(User.objects.filter(username="example_client").exists())

    def test_user_modify(self):
        new_username = "my_new_nick"
        self.user.username = new_username
        self.user.save()
        self.assertEqual(self.user.username, new_username)

    def test_user_delete(self):
        self.user.delete()
        self.assertFalse(User.objects.filter(username="example_client").exists())

    def test_user_login(self):
        # response = self.client.post('/core/login/', {'username': 'example_client', 'password': 'admin'})
        response = self.client.post('/login/', {'username': 'example_client', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)  # Sprawdzam, czy żądanie logowania zostało pomyślnie przetworzone.
        self.assertTrue('user' in response.context)  # Sprawdzam, czy użytkownik jest dostępny w kontekście widoku.
        self.assertTrue(response.context['user'].is_authenticated)  # Sprawdzam, czy użytkownik jest uwierzytelniony.
