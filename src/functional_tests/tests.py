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

		# He also notices the tab title "J&J's Wedding Roll"
		title = self.browser.title
		self.assertEqual("J&J's Wedding Roll",title)
		
		# Below, there is a login form which asks for an email
		# address and password and a submit button below it.
		login_email_field = self.browser.find_element_by_id('id_email')
		login_password_field = self.browser.find_element_by_id('id_password')
		login_submit_button = self.browser.find_element_by_id('id_submit_button')
		self.assertEqual('Login',login_submit_button.get_attribute("innerHTML"))

		# He also sees a link for new user signup
		signup_link = self.browser.find_element_by_link_text('Signup')

		# Since, he has never used it before, he clicks on Signup
		signup_link.click()

		# He is redirected to a registration page
		curr_url = self.browser.current_url
		self.assertEqual(curr_url,self.BASE_URL+'/signup/')
		
		# He sees three form fields this time:
		# One asks for his email, while the other two are
		# password and password confirmation fields along with a 
		# Signup Button

		signup_email_field = self.browser.find_element_by_id('id_email')
		signup_password1_field = self.browser.find_element_by_id('id_password1')
		signup_password2_field = self.browser.find_element_by_id('id_password2')
		signup_submit_button = self.browser.find_element_by_id('id_submit_button')
		self.assertEqual('SignUp',signup_submit_button.get_attribute("innerHTML"))

		#self.fail(msg='Test Not Complete')