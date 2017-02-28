from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from webhub.views import dashboard
from webhub.checker import check

class PcuserTest(LiveServerTestCase):

	"""
	Tests to check the Pcusers
	The following checks are performed:
		- pcuser is only able to login through the homepage
		- Pcuser must be able to see the dashboard
			- which must show his/her username
			- the correct links
			- logout button
			- correct texts
		- correct page rendering and message after logout
		- correct page rendering after clicking on several links
	"""

	def setUp(self):

		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(5)

		self.user_1 = User.objects.create_superuser(
						username='testpcuser',
						email='testpcuser@gmail.com',
						password='password'
						)

		self.pcuser_1 = Pcuser.objects.create(
							user=user_1,
							location='some random location',
							phone='+9876543262',
							gender='Male',
							reset_pass='1',
							verified='1'
							)

		self.pcuser_1.save()

		self.user_2 = User.objects.create_superuser(
						username='testpcuser2',
						email='testpcuser2@gmail.com',
						password='password'
						)

		self.pcuser_2 = Pcuser.objects.create(
							user=user_2,
							location='some random location 2',
							phone='+9876544262',
							gender='Female',
							reset_pass='1',
							verified='1'
							)
		self.pcuser_2.save()

	def tearDown(self):
		self.browser.quit()

	def test_the_homepage_for_pcuser(self):
		#pcuser opens the browser, and navigates to the homepage
		self.browser.get(self.live_server_url)
		#user sees the correct title and body elements along with the links
		title = self.browser.find_element_by_tag_name('title')
		self.assertIn('Welcome !', title.text)
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Mobile App Control Center', body.text)
		self.assertIn('Welcome, !', body.text)
		self.assertIn('Logout', body.text)
		self.assertIn('Go to PCSA', body.text)
		self.assertIn('Go to Malaria', body.text)

	def test_correct_template_is_rendered(self):
		found = resolve('/')
		self.assertEqual(found.func, dashbaord)

	def template_shows_correct_info(self):
		request = HttpRequest()
		response = dashboard(request)
		self.assertIn(b'<<h3><a href="/malaria/list_posts/">Malaria</a></h3>' response.content)
		self.assertIn(b'<h3><a href="/pcsa/list_posts/">PCSA</a></h3>', response.content)
		self.assertIn(b'<title>DashBoard</title>', response.content)
		self.assertIn(b'<h1>PEACE CORPS HUB</h1>', response.content)

	def test_logout_then_login_again(self):
		#pcuser decides to log out from the dashboard
		logout_button = self.browser.find_element_by_link_text('Logout')
		logout_button.click()
		#the user must be redirected to the login page
		#user must see the required login details
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Log in', body.text)
		username_field = self.browser.find_element_by_name('username')
		self.assertIn(username_field, body.text)
		password_field = self.browser.find_element_by_name('password')
		self.assertIn(password_field, body.tetx)
		
	def test_login_with_correct_credentials(self):
		#pcuser enters the correct credentials
		self.browser.get(self.live_server_url)
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Log in', body.text)
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testpcuser')
		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys('password')
		password_field.send_keys(Keys.ENTER)
		new_body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Mobile App Control Center', new_body.text)
		self.assertIn('Welcome, !', new_body.text)
		self.assertIn('Logout', new_body.text)
		self.assertIn('Go to Malaria', new_body.text)
		self.assertIn('Go to PCSA', new_body.text)

	def test_login_with_incorrect_credentials(self):
		#pcuser enters the incorrect credentials
		self.browser.get(self.live_server_url)
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Log in', body.text)
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testpcuser')
		username_field.send_keys(Keys.ENTER)
		password_field = self.browser.find_element_by_tag_name('password')
		password_field.send_keys('wrong_password')
		password_field.send_keys(Keys.ENTER)
		#error message must be shown. 
		new_body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Please enter the correct login credentials', new_body.text)
		self.assertNotIn('Logout', new_body.text)

	
