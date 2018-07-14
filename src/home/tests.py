from django.test import TestCase

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