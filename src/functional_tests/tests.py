# FUNCTIONAL TESTS INVOLVING USER STORIES

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class LiveTest(LiveServerTestCase):
	# LiveServerTestCase creates it's own development server
	def setUp(self):
		self.BASE_URL = self.live_server_url
		# For Mac/Linux, chrome webdriver should be in PATH or in usr/local/bin
		# For Windows, you can pass the path of the driver
		# using executable_path=<path>/chromedriver.exe
		self.browser = webdriver.Chrome()

	def tearDown(self):
		self.browser.quit()

	def test_new_user(self):
		'''
		Tests a new user functionality for signup and login
		'''

		# Adam had attended Joe's wedding.
		# Joe told him that he had created a website which
		# allows people to upload and share the wedding photos.

		# Intrigued, he goes to the url Joe mentioned.
		self.browser.get(self.BASE_URL)

		# He is greeted by a welcome page.
		# The page says: "Welcome to Jane and Joe's Wedding Album"
		tag = self.browser.find_element_by_tag_name('body')
		self.assertIn("Welcome to Jane and Joe's Wedding Album",tag.text)
		
		# Below, there is a login form which asks for an email
		# address and password.
		# He also notices the tab title "J&J's Wedding Roll"

		#self.fail(msg='Test Not Complete')