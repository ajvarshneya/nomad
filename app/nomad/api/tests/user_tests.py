from django.test import TestCase, Client
from django.forms.models import model_to_dict
from api.models import *
import json

def get_response_result(json_response):
	return json.loads(json_response.content.decode('utf-8'))['result']

# Create your tests here.
class UserApiTests(TestCase):
	fixtures = ['db']

	def test_user_index(self):
		response = self.client.get('/api/v1/users/')

		self.assertEqual(response.status_code, 200)

		# Get json data from response
		json_result = get_response_result(response)

		# Check that 4 models were returned
		self.assertEqual(len(json_result), 4)

	def test_user_detail_get_valid(self):
		user_id = 1
		user = User.objects.get(pk=user_id)
		user_dict = model_to_dict(user)

		response = self.client.get('/api/v1/users/' + str(user_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_response_result(response)
		# Compare all result fields to those in the model
		for key in json_result:
			self.assertEqual(json_result[key], str(user_dict[key]))

	def test_user_detail_post_valid(self):
		user_id = 1
		user = User.objects.get(pk=user_id)
		data = model_to_dict(user)
		data['first_name'] = "new first name"
		data['last_name'] = "new last name"

		response = self.client.post('/api/v1/users/' + str(user_id) + '/', data)

		self.assertEqual(response.status_code, 200)

		# Get updated model
		user = User.objects.get(pk=user_id)
		user_dict = model_to_dict(user)

		json_result = get_response_result(response)

		# Compare all result fields to those in the model 
		for key in json_result:
			self.assertEqual(json_result[key], user_dict[key])

	def test_user_detail_delete_valid(self):
		user_id = 1
		response = self.client.delete('/api/v1/users/' + str(user_id) + '/')

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
			'zipcode': "12345",
		}
		response = self.client.post('/api/v1/users/create/', data)

		self.assertEqual(response.status_code, 200)

		json_result = get_response_result(response)

		# Get the new user model
		user_id = json_result['id']
		user = User.objects.get(pk=user_id)
		user_dict = model_to_dict(user)

		# Compare all result fields to those in the model
		for key in json_result:
			self.assertEqual(json_result[key], user_dict[key])

		for key in data:
			self.assertEqual(data[key], user_dict[key])