import os
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from users.models import UserAuth
# Create your tests here.

class HomePageAndSignup(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_home_page_is_served_on_root(self):
        # ask for home page
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home/index.html')


    def test_signup_page_is_served(self):
        response = self.client.get('/signup/')
        self.assertTemplateUsed(response,'home/signup.html')

    def test_signup_page_account_creation_redirects_to_home(self):
        response = self.client.post('/signup/',{'email':'adam200@gmail.com',
            'password1':'password123','password2':'password123'})
        # after succesful post request, it should redirect to home page
        # status code will be 200 if form is not valid
        # status code will be 405 if post method is forbidden
        self.assertRedirects(response,'/',status_code=302,target_status_code=200)


    def test_signup_page_creates_db_entry_on_valid_data(self):
        # move it to users.tests
        response = self.client.post('/signup/',{'email':'adam2000@gmail.com',
            'password1':'password123','password2':'password123'})
        try:
            obj = UserAuth.objects.get(email='adam2000@gmail.com')
        except ObjectDoesNotExist:
            self.assertTrue(False,'Entry was not created in DB')

    def test_signup_page_rejects_different_passwords_and_redirects_to_signup(self):
        response = self.client.post('/signup/',{'email':'adam2000@gmail.com',
            'password1':'password123','password2':'password12'})

        self.assertRedirects(response,'/signup/',status_code=302,target_status_code=200)

    def test_signup_page_does_not_create_db_on_invalid_data(self):
        response = self.client.post('/signup/',{'email':'adam2000gmail.com',
            'password1':'password123','password2':'password12'})
        flag=False
        try:
            obj = UserAuth.objects.get(email='adam2000@gmail.com')
        except ObjectDoesNotExist:
            flag=True
        self.assertTrue(flag,'Object was created')


class UserLogin(TestCase):
    def setUp(self):
        # If make_password is not used then the password gets stored as plain text
        self.user = UserAuth.objects.create(email='user1@email.com',
                                            password=make_password('password123'))

    def test_does_not_authenticate_unregistered_user(self):
        retval = authenticate(username='user2@email.com',password='password123')
        self.assertEqual(retval,None)

    def test_does_not_authenticate_invalid_combination(self):
        retval = authenticate(username='user1@email.com',password='password1')
        self.assertEqual(retval,None)


    def test_authenticates_registered_user(self):
        retval = authenticate(username='user1@email.com',password='password123')
        self.assertEqual(retval,self.user)


    def test_login_page_redirects_to_rolls_home_on_succesful_login(self):
        response = self.client.post('/',{'email':'user1@email.com',
                                         'password':'password123'})
        self.assertRedirects(response,'/roll/',status_code=302,target_status_code=200)

    def test_login_after_successful_authentication(self):
        response = self.client.post('/', 
                                    {'email':'user1@email.com',
                                     'password':'password123'}, follow=True)
        self.assertTrue(response.context['user'].is_active)
        

class PhotoUpload(TestCase):
    def setUp(self):
        self.Client = Client()
        self.image_path = os.path.join(os.getcwd(),'image.jpeg')
        self.not_image_path = os.path.join(os.getcwd(),'manage.py')
        # Since UploadForm accepts an image, a test image needs to be loaded
        self.image = SimpleUploadedFile(name='image.jpeg',
                                            content=open(self.image_path,
                                                         'rb').read(),
                                           content_type='image/jpeg')
        self.not_image = SimpleUploadedFile(name='readme.txt',
                                            content=open(self.not_image_path,
                                                         'rb').read(),
                                           content_type='text/plain')
        # The upload form's view requires a user, hence logging one in
        user = UserAuth.objects.create(email='testuser@email.com',
                                       password=make_password('password123'))
        user.save()
        self.client.login(username='testuser@email.com', password='password123')
        
    def test_view_function_accepts_image_on_upload(self):
        response = self.client.post('/roll/upload/',{'photo_url':self.image},follow=True)
        self.assertRedirects(response,'/roll/',status_code=302,target_status_code=200)
        self.assertTemplateUsed(response,'rolls/home.html')

    def test_view_function_rejects_non_image_file_on_upload(self):
        response = self.client.post('/roll/upload/',{'photo_url':self.not_image},follow=True)
        # If it is a redirect, response does not contain a template
        self.assertTemplateUsed(response,'rolls/upload.html')

class Logout(TestCase):
    def setUp(self):
        user = UserAuth.objects.create(email='testuser@email.com',
                                       password=make_password('password123'))
        user.save()
        self.client.login(username='testuser@email.com', password='password123')

    def test_logged_in_user_is_logged_out(self):
        response = self.client.get('/logout/',follow=True)
        self.assertRedirects(response,'/',status_code=302,target_status_code=200)
        self.assertIsInstance(response.context['user'],AnonymousUser)