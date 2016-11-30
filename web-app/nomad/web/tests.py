from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import os
import re
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
		self.assertIn('Logout', selenium.page_source)
		self.assertIn('User', selenium.page_source)
		self.assertNotIn('Login', selenium.page_source)

	def test_logout(self):
		selenium = self.selenium

		# Login
		url = self.format_live_server_url('web:auth-login')
		selenium.get(url)
		selenium.find_element_by_id('id_username').send_keys('ironman')
		selenium.find_element_by_id('id_password').send_keys('password')
		selenium.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.RETURN)

		# Check that login worked properly
		self.assertIn('Logout', selenium.page_source)
		self.assertIn('User', selenium.page_source)

		# Click the logout button
		logout = selenium.find_element_by_link_text('Logout')
		logout.click()

		# Check that logout worked properly
		self.assertNotIn('Logout', selenium.page_source)
		self.assertNotIn('User', selenium.page_source)
		self.assertIn('Login', selenium.page_source)

	def test_search_results(self):
		selenium = self.selenium

		# Get the home screen
		url = self.format_live_server_url('web:index')
		selenium.get(url)

		# Find search bar
		search_bar = selenium.find_element_by_name('query')

		# Search for all locations in the US
		search_bar.send_keys('US')
		search_bar.send_keys(Keys.RETURN)

		# Check that the search page loaded with results
		self.assertIn('Listings', selenium.page_source)
		
		# Check that each item links to a item detail page
		items = selenium.find_elements_by_class_name('list-group-item')
		listing_url_exp = re.compile(r'/listings/\d+/')
		for item in items:
			item_url = item.get_attribute('href')
			self.assertTrue(listing_url_exp.search(item_url))

	def test_search_results_empty(self):
		selenium = self.selenium

		# Get the home screen
		url = self.format_live_server_url('web:index')
		selenium.get(url)

		# Find search bar
		search_bar = selenium.find_element_by_name('query')

		# Search for an invalid query
		search_bar.send_keys('ZZ')
		search_bar.send_keys(Keys.RETURN)

		# Check that the search page loaded with empty results message
		self.assertIn('Listings', selenium.page_source)
		self.assertIn('No results found', selenium.page_source)

	def test_most_recent_listings(self):
		selenium = self.selenium

		# Get the home screen
		url = self.format_live_server_url('web:index')
		selenium.get(url)

		# Find the cols in the row under the 'Most Recent' header
		cols = selenium.find_elements_by_xpath("//h3[text()='Most Recent']/following-sibling::div[1]/child::*")
		for i in range(len(cols)):
			col = selenium.find_element_by_xpath("//h3[text()='Most Recent']/following-sibling::div[1]/child::*[" + str(i+1) + "]")

			# Get the item title
			listing_title = col.text

			# Click the link
			col.click()

			# Check that the new page has detail information
			self.assertIn(listing_title, selenium.page_source)
			self.assertIn('Info', selenium.page_source)
			self.assertIn('Address', selenium.page_source)
			self.assertIn('Reviews', selenium.page_source)

			# Go back
			selenium.back()

	def test_most_popular_listings(self):
		selenium = self.selenium

		# Get the home screen
		url = self.format_live_server_url('web:index')
		selenium.get(url)

		# Find the cols in the row under the 'Most Popular' header
		cols = selenium.find_elements_by_xpath("//h3[text()='Most Popular']/following-sibling::div[1]/child::*")
		for i in range(len(cols)):
			col = selenium.find_element_by_xpath("//h3[text()='Most Popular']/following-sibling::div[1]/child::*[" + str(i+1) + "]")

			# Get the item title
			listing_title = col.text

			# Click the link
			col.click()

			# Check that the new page has detail information
			self.assertIn(listing_title, selenium.page_source)
			self.assertIn('Info', selenium.page_source)
			self.assertIn('Address', selenium.page_source)
			self.assertIn('Reviews', selenium.page_source)

			# Go back
			selenium.back()

	def test_create_listing(self):
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
		self.assertIn('Logout', selenium.page_source)
		self.assertIn('User', selenium.page_source)
		self.assertNotIn('Login', selenium.page_source)

		url = self.format_live_server_url("web:listings-create")
		selenium.get(url)

		submit = selenium.find_element_by_xpath("//input[@type='submit']")
		listing_title = selenium.find_element_by_id('id_title')
		listing_street = selenium.find_element_by_id('id_street')
		listing_city = selenium.find_element_by_id('id_city')
		listing_country = selenium.find_element_by_id('id_country')
		listing_zip = selenium.find_element_by_id('id_zipcode')
		listing_beds = selenium.find_element_by_id('id_beds')
		listing_baths = selenium.find_element_by_id('id_baths')
		listing_price = selenium.find_element_by_id('id_price')

		listing_title.send_keys('Testing Listing')
		listing_street.send_keys('Testing Street')
		listing_city.send_keys('Testing City')
		listing_country.send_keys('Testing Country')
		listing_zip.send_keys('90210')
		listing_beds.send_keys('99')
		listing_baths.send_keys('99')
		listing_price.send_keys('1337')
		submit.send_keys(Keys.RETURN)

		self.assertIn('Info', selenium.page_source)
		self.assertIn('Address', selenium.page_source)
		self.assertIn('Reviews', selenium.page_source)

		self.assertIn('Testing Listing', selenium.page_source)
		self.assertIn('Testing Street', selenium.page_source)
		self.assertIn('Testing City', selenium.page_source)
		self.assertIn('Testing Country', selenium.page_source)
		self.assertIn('90210', selenium.page_source)
		self.assertIn('99', selenium.page_source)
		self.assertIn('1337', selenium.page_source)

def test_logout_from_listing(self):
		selenium = self.selenium

		# Get listing screen
		url = 'http://localhost:8000/listings/1/'
		selenium.get(url)



		# Click login
		login = selenium.find_element_by_link_text('Login')
		login.click()

		# Find form elements
		username = selenium.find_element_by_id('id_username')
		password = selenium.find_element_by_id('id_password')
		submit = selenium.find_element_by_xpath("//input[@type='submit']")

		# Submit the login form
		username.send_keys('ironman')
		password.send_keys('password')
		submit.send_keys(Keys.RETURN)

		#Logout
		login = selenium.find_element_by_link_text('Logout')
		login.click()


		#Check
		self.assertIn('Info', selenium.page_source)
		self.assertIn('Address', selenium.page_source)
		self.assertIn('Reviews', selenium.page_source)

		self.assertIn('Beach House', selenium.page_source)
		self.assertIn('beach street', selenium.page_source)
		self.assertIn('beach city', selenium.page_source)
		self.assertIn('US', selenium.page_source)
		self.assertIn('12345', selenium.page_source)
		self.assertIn('4', selenium.page_source)
		self.assertIn('4.5', selenium.page_source)

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
