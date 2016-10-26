from django.test import TestCase, Client
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.contrib.auth import hashers
from models.models import *
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

# Create your tests here.
class UserApiTests(TestCase):
	fixtures = ['db']

	# Helper method to compare fields in a json result and a user model
	def compare_fields(self, json_result, user):
		for key in json_result:
			# Handle profile images explicitly
			if key == "profile_image":
				self.assertEqual(json_result[key]["url_full"], user.profile_image.url_full)
			else:
				self.assertEqual(json_result[key], getattr(user, key))

	def test_user_index(self):
		url = reverse('models:users-index')
		response = self.client.get(url)
		users = User.objects.all()

		self.assertEqual(response.status_code, 200)

		# Get json data from response
		json_result = get_json_response(response)['result']

		# Check that all models were returned
		self.assertEqual(len(json_result), len(users))

	def test_user_detail_get_valid(self):
		user_id = 1
		user = User.objects.get(pk=user_id)

		url = reverse('models:users-detail', kwargs={'user_id': user_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# # Compare all result fields to those in the model
		self.compare_fields(json_result, user)

	def test_user_detail_get_invalid(self):
		user_id = 0

		url = reverse('models:users-detail', kwargs={'user_id': user_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_user_detail_post_valid(self):
		user_id = 1
		user = User.objects.get(pk=user_id)
		data = model_to_dict(user)
		data['first_name'] = "new first name"
		data['last_name'] = "new last name"

		url = reverse('models:users-detail', kwargs={'user_id': user_id})
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		# Get updated model
		user = User.objects.get(pk=user_id)

		json_result = get_json_response(response)['result']

		# Compare all result fields to those in the model 
		self.compare_fields(json_result, user)

	def test_user_detail_post_invalid_id(self):
		user_id = 0

		# Get data for a user in the database
		user = User.objects.all()[0]
		data = model_to_dict(user)
		data.pop('id', None)
		data['first_name'] = "new first name"
		data['last_name'] = "new last name"

		url = reverse('models:users-detail', kwargs={'user_id': user_id})
		response = self.client.post(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_user_detail_post_invalid_data(self):
		# Assumes all fields should be passed in a post method
		user_id = 1
		user = User.objects.get(pk=user_id)
		data = model_to_dict(user)
		data.pop('first_name', None)
		data.pop('last_name', None)

		url = reverse('models:users-detail', kwargs={'user_id': user_id})
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and form error message
		self.assertEqual(json_response["ok"], False)
		errors = json_response["error"]
		for field in errors:
			self.assertIn("This field is required.", errors[field])

	def test_user_detail_delete_valid(self):
		user_id = 1
		url = reverse('models:users-detail', kwargs={'user_id': user_id})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(json_result['id'], str(user_id))

	def test_user_detail_delete_invalid(self):
		user_id = 0
		url = reverse('models:users-detail', kwargs={'user_id': user_id})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_user_create_valid(self):
		data = {
			'first_name': "first",
			'last_name': "last",
			'email': "a@example.com",
			'phone_number': "1234567890",
			'password': "password",
			'username': "sample_user",
			'creditcard': "4111111111111111",
			'street': "123 example lane",
			'city': "somewhere",
			'country': "US",
			'zipcode': "12345"
		}
		url = reverse('models:users-create')
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# Get the new user model
		user_id = json_result['id']
		user = User.objects.get(pk=user_id)

		# Compare all result fields to those in the model
		self.compare_fields(json_result, user)

		# Compare all data fields to those in the model
		for key in data:
			if key == "password":
				hashers.check_password(data[key], user.password)
			else:
				self.assertEqual(data[key], getattr(user, key))

	def test_user_create_invalid(self):
		data = {
			# 'first_name': "first",
			# 'last_name': "last",
			'email': "a@example.com",
			'phone_number': "1234567890",
			'password': "password",
			'username': "sample_user",
			'creditcard': "4111111111111111",
			'street': "123 example lane",
			'city': "somewhere",
			'country': "US",
			'zipcode': "12345"
		}
		url = reverse('models:users-create')
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and form error message
		self.assertEqual(json_response["ok"], False)
		errors = json_response["error"]
		for field in errors:
			self.assertIn("This field is required.", errors[field])