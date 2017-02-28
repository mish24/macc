from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from django.test import LiveServerTestCase, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from webhub.views import dashboard
from webhub.checker import check

class AdminTest(LiveServerTestCase):

	"""
	Contains test for the home page and user suite
	The following checks are performed
	- checks homepage contains correct links
	- correct templates are urls are used
	- even user isn't able to access the site first
	- correct user details only access admin site
	- correct error info is shown
	- user is able to create a pcuser
	"""

	def setUp(self):
		self.browser = webdriver.Firefox()

		self.user_1 = User.objects.create_superuser(
						username='testadmin',
						email='test@gmail.com',
						password='password'
						)
		self.user_1.save()

		self.user_2 = User.objects.create_superuser(
						username='testadmin2',
						email='test2@gmail.com',
						password='password'
						)
		self.user_2.save()


	def tearDown(self):
		self.browser.quit()


	def test_the_homePage(self):
		#user just opens the browser, navigates to the homepage
		self.browser.get(self.live_server_url)
		#user sees the correct title and body elements
		title = self.browser.find_element_by_tag_name('title')
		self.assertIn('Welcome !', title.text)
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Mobile App Control Center', body.text)
		self.assertIn('Log in', body.text)
		self.assertIn('Username', body.text)
		self.assertIn('Password', body.text)
		self.assertIn('New User ?', body.text)


	def test_correct_template_is_rendered(self):

		found = resolve('/')
		self.assertEqual(found.func , dashboard)

	def test_template_shows_correct_info(self):
		request = HttpRequest()
		response = dashboard(request)
		self.assertIn(response.content.startwith(b'<html>'))
		self.assertIn(b'<title>DashBoard</title>', response.content)
		self.assertIn(response.content.endswith(b'</html>'))


	def test_admin_login_page(self):
		#user decides to login as the admin
		#goes to the admin link
		self.browser.get(self.live_server_url + '/admin/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Django administration', body.text)


	def test_admin_correct_credentials(self):
		#user decides to login as the admin
		self.browser.get(self.live_server_url + '/admin/')
		body = self.browser.find_element_by_tag_name('body')
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testadmin')
		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys('password')
		password_field.send_keys(Keys.ENTER)
		#login credentials are correct, user is redirected to main 
		#administration page
		new_body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Site administration', new_body.text)

		#user decides to login as the admin
		self.browser.get(self.live_server_url + '/admin/')
		body = self.browser.find_element_by_tag_name('body')
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testadmin2')
		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys('password')
		password_field.send_keys(Keys.ENTER)
		#login credentials are correct, user is redirected to main 
		#administration page
		new_body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Site administration', new_body.text)


	def test_wrong_admin_credentials_dont_redirect(self):
		#user shouldn't be able to login
		#error message must be shown
		self.browser.get(self.live_server_url + '/admin/')
		body = self.browser.find_element_by_tag_name('body')
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testadmin')
		password_field = self.browser.find_element_by_name('wrong_password')
		password_field.send_keys(Keys.ENTER)
		#wrong login creedentials entered
		#user stays on the same page
		new_body = self.browser.find_element_by_tag_name('body')
		self.assertNotIn('Site administration', new_body.text)
		self.assertIn('Log in', new_body.text)

		#user shouldn't be able to login
		#error message must be shown
		self.browser.get(self.live_server_url + '/admin/')
		body = self.browser.find_element_by_tag_name('body')
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testadmin2')
		password_field = self.browser.find_element_by_name('wrong_password')
		password_field.send_keys(Keys.ENTER)
		#wrong login creedentials entered
		#user stays on the same page
		new_body = self.browser.find_element_by_tag_name('body')
		self.assertNotIn('Site administration', new_body.text)
		self.assertIn('Log in', new_body.text)

	def test_user_can_create_pcuser(self):
		#user should be able to create new pcuser
		#all required fields must be present
		self.browser.get(self.live_server_url + '/admin/')
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testadmin')
		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys('password')
		password_field.send_keys(Keys.ENTER)

		#user clicks on the pcuser link
		pcusers_link = self.browser.find_element_by_link_text('Pcusers')
		pcusers_link[0].click()

		#user clicks on the Add Pcuser link
		add_pcuser_link = self.browser.find_element_by_link_text('Add Pcuser')
		add_pcuser_link.click()

		#user fills out the form
		#user sees the users list in the dropdown and selects his/her name
		users_link = self.browser.find_element_by_name('Users')
		for option in users_link.find_element_by_tag_name('option'):
			if option.text == 'user_1':
				option.click()
		self.browser.find_element_by_name('location').send_keys('Some random location')
		self.browser.find_element_by_name('phone').send_keys('+98765432')
		#user selects the gender from the dropdown
		gender_link = self.browser.find_element_by_name('gender')
		for option in gender_link.find_element_by_tag_name('option'):
			if option.text == 'Female':
				option.click()
		self.browser.find_element_by_name('reset_pass').send_keys('1')
		self.browser.find_element_by_name('verified').send_keys('1')
		#user clicks on the save button
		self.browser.find_element_by_css_selector("input[value='Save']").click()
		#the pcuser has been added
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('user_1', body.text)

		#user logs out 
		logout_button = self.browser.find_element_by_link_text('Log out')
		logout_button.click()

		#user must see the message django-1.6 shows
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Thanks for spending some quality time with the web site today', body.text)





