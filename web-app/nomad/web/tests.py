from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import os
import socket

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8004'

# Integration test setup base from StackOverflow:
# http://stackoverflow.com/questions/32408429/running-django-tests-with-selenium-in-docker

# Use LiveServerTestCase to render the html
class IntegrationTests(LiveServerTestCase):
	live_server_url = 'http://{}:8004'.format(
	    socket.gethostbyname(socket.gethostname())
	)

	def format_live_server_url(self, web_url):
		return self.live_server_url + reverse(web_url)

	def setUp(self):
		# settings.DEBUG = True
		self.selenium = webdriver.Remote(
			command_executor="http://selenium:4444/wd/hub",
			desired_capabilities=DesiredCapabilities.CHROME
		)

	def tearDown(self):
		self.selenium.quit()
		super().tearDown()

	def test_login(self):
		selenium = self.selenium

		# Get login screen
		url = self.format_live_server_url("web:auth-login")
		selenium.get(url)

		# Find form elements
		username = selenium.find_element_by_id('id_username')
		password = selenium.find_element_by_id('id_password')
		submit = selenium.find_element_by_xpath("//input[@type='submit']")

		# Submit the login form
		username.send_keys('ironman')
		password.send_keys('password')
		submit.send_keys(Keys.RETURN)

		# Check that the user is signed in
		# print(selenium.page_source)
		self.assertIn('Logout', selenium.page_source)
		self.assertIn('User', selenium.page_source)
		self.assertNotIn('Login', selenium.page_source)

# Create your tests here.
class HomeViewTests(TestCase):
	def test_index_view_valid(self):
		"""
		Check for valid response
		"""
		response = self.client.get(reverse("web:index"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Nomad")

class ListingViewTests(TestCase):
	def test_index_view_valid(self):
		"""
		Check for valid response with 1+ views
		"""
		response = self.client.get(reverse("web:listings-index"))
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, "No listings found")

	def test_detail_view_valid(self):
		"""
		Check for valid response with valid listing id
		"""
		url = reverse("web:listings-detail", kwargs={'listing_id': 1})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_detail_view_invalid(self):
		"""
		Check for 404 page with invalid listing id
		"""
		# listing id can never be 0, so use that as the invalid id
		url = reverse("web:listings-detail", kwargs={'listing_id': 0})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
