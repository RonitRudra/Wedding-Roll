import os
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from users.models import UserAuth

# Create your tests here.
class ViewGetLoggedIn(TestCase):
    """
    Test access rights of logged in user
    """
    def setUp(self):
        user = UserAuth.objects.create(email='testuser@email.com',
                                       password=make_password('password123'))
        user.save()
        self.client.login(username='testuser@email.com', password='password123')

    def test_home_serves_correct_html(self):
        response = self.client.get('/roll/',follow=True)
        self.assertTemplateUsed(response,'rolls/home.html')

    def test_upload_serves_correct_html(self):
        response = self.client.get('/roll/upload/')
        self.assertTemplateUsed(response,'rolls/upload.html')

    def test_manage_redirects_to_rolls_for_not_owner(self):
        response = self.client.get('/roll/manage/')
        self.assertRedirects(response,'/roll/')

    def test_login_redirects_to_roll(self):
        response = self.client.get('/login/')
        self.assertRedirects(response,'/roll/')

    def test_login_redirects_to_roll(self):
        response = self.client.get('/signup/')
        self.assertRedirects(response,'/roll/')


class ViewGetOwner(TestCase):
    def setUp(self):
        user = UserAuth.objects.create(email='testuser@email.com',
                                       password=make_password('password123'))
        user.is_owner=True
        user.save()
        self.client.login(username='testuser@email.com', password='password123')

    def test_manage_allows_owner_to_access(self):
        response = self.client.get('/roll/manage/')
        self.assertTemplateUsed(response,'rolls/manage.html')

class ViewGetAnonymous(TestCase):

    def test_home_redirects(self):
        response = self.client.get('/roll/',follow=True)
        self.assertRedirects(response,'/login/')

    def test_upload_redirects(self):
        response = self.client.get('/roll/upload/')
        self.assertRedirects(response,'/login/')
    
    def test_manage_redirects(self):
        response = self.client.get('/roll/manage/')
        self.assertRedirects(response,'/login/')