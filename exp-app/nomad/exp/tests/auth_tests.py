from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from datetime import datetime
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class AuthExpTests(TestCase):
	def test_login_valid(self):
		url = reverse("exp:auth-login")
		data = {
			"username" : "ironman",
			"password" : "password"
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

	def test_login_invalid(self):
		url = reverse("exp:auth-login")
		data = {
			"username" : "ironman",
			"password" : "notthepassword"
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertFalse(json_response["ok"])

	def test_logout_valid(self):
		# Log in
		url = reverse("exp:auth-login")
		data = {
			"username" : "ironman",
			"password" : "password"
		}
		response = self.client.post(url, data)
		json_response = get_json_response(response)

		# Log out
		url = reverse("exp:auth-logout")
		data = {
			"authenticator" : json_response["result"]["authenticator"]
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

	def test_logout_invalid(self):
		# Log out
		url = reverse("exp:auth-logout")
		data = {
			"authenticator" : "garbagestring"
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertFalse(json_response["ok"])

	def test_create_user_valid(self):
		# Log in
		url = reverse("exp:auth-create-user")
		data = {
		    "country": "US",
		    "last_name": "last",
		    "creditcard": "4111111111111111",
		    "email": "a@example.com",
		    "id": 8,
		    "zipcode": "12345",
		    "street": "123 example lane",
		    "first_name": "first",
		    "city": "somewhere",
		    "username": "sample_user",
		    "phone_number": "1234567890",
		    "password": "password"
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

	def test_create_user_invalid(self):
		# Log in
		url = reverse("exp:auth-create-user")
		data = {
		    "country": "US",
		    "last_name": "last",
		    "creditcard": "4111111111111111",
		    "email": "a@example.com",
		    "id": 8,
		    "zipcode": "12345",
		    "street": "123 example lane",
		    "first_name": "first",
		    "city": "somewhere",
		    "username": "sample_user",
		    "phone_number": "1234567890",
		    # "password": "password"
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertFalse(json_response["ok"])
