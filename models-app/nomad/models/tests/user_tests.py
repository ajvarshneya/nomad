from django.test import TestCase, Client
from django.forms.models import model_to_dict
from models.models import *
import json

def get_response_result(json_response):
	return json.loads(json_response.content.decode('utf-8'))['result']

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
		response = self.client.get('/models/api/v1/users/')
		users = User.objects.all()

		self.assertEqual(response.status_code, 200)

		# Get json data from response
		json_result = get_response_result(response)

		# Check that all models were returned
		self.assertEqual(len(json_result), len(users))

	def test_user_detail_get_valid(self):
		user_id = 1
		user = User.objects.get(pk=user_id)

		response = self.client.get('/models/api/v1/users/' + str(user_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_response_result(response)

		# # Compare all result fields to those in the model
		self.compare_fields(json_result, user)

	def test_user_detail_post_valid(self):
		user_id = 1
		user = User.objects.get(pk=user_id)
		data = model_to_dict(user)
		data['first_name'] = "new first name"
		data['last_name'] = "new last name"

		response = self.client.post('/models/api/v1/users/' + str(user_id) + '/', data)

		self.assertEqual(response.status_code, 200)

		# Get updated model
		user = User.objects.get(pk=user_id)

		json_result = get_response_result(response)

		# Compare all result fields to those in the model 
		self.compare_fields(json_result, user)

	def test_user_detail_delete_valid(self):
		user_id = 1
		response = self.client.delete('/models/api/v1/users/' + str(user_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_response_result(response)
		self.assertEqual(json_result['id'], str(user_id))

	def test_user_create(self):
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
		response = self.client.post('/models/api/v1/users/create/', data)

		self.assertEqual(response.status_code, 200)

		json_result = get_response_result(response)

		# Get the new user model
		user_id = json_result['id']
		user = User.objects.get(pk=user_id)

		# Compare all result fields to those in the model
		self.compare_fields(json_result, user)

		# Compare all data fields to those in the model
		for key in data:
			self.assertEqual(data[key], getattr(user, key))