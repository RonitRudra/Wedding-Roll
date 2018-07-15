from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from users.models import UserAuth

# Create your tests here.

class HomeTest(TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_signup_page_creates_db_entry(self):
		response = self.client.post('/signup/',{'email':'adam2000@gmail.com',
			'password1':'password123','password2':'password123'})
		try:
			obj = UserAuth.objects.get(email='adam2000@gmail.com')
		except ObjectDoesNotExist:
			self.assertTrue(False,'Entry was not created in DB')
