from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserAuth

# Create your tests here.

class HomeTest(TestCase):

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

	def test_signup_page_creates_db_entry(self):
		response = self.client.post('/signup/',{'email':'adam2000@gmail.com',
			'password1':'password123','password2':'password123'})
		try:
			obj = UserAuth.objects.get(email='adam2000@gmail.com')
		except ObjectDoesNotExist:
			self.assertTrue(False,'Entry was not created in DB')
