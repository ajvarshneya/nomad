from django.test import TestCase, Client
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from models.models import *
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class AuthenticatorApiTests(TestCase):
	fixtures = ['db']

	def test_auth_check_valid(self):
		auth_model = Authenticator.objects.all()[0]
		authenticator = auth_model.authenticator

		url = reverse('models:auth-check', kwargs={'authenticator': authenticator})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(int(json_result['user']), auth_model.user.id)
		self.assertEqual(json_result['authenticator'], authenticator)

	def test_auth_check_invalid(self):
		authenticator = "invalidauth"

		url = reverse('models:auth-check', kwargs={'authenticator': authenticator})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_auth_create_new(self):
		user_id = 3
		url = reverse('models:auth-create', kwargs={'user_id': user_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(int(json_result['user']), user_id)
		self.assertIsNotNone(json_result['authenticator'])

	def test_auth_create_existing(self):
		auth_model = Authenticator.objects.all()[0]
		user_id = auth_model.user.id

		url = reverse('models:auth-create', kwargs={'user_id': user_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(json_result['user'], user_id)
		self.assertEqual(json_result['authenticator'], auth_model.authenticator)

	def test_auth_delete_valid(self):
		# Get an auth model from the db
		auth_model = Authenticator.objects.all()[0]
		authenticator = auth_model.authenticator

		url = reverse('models:auth-delete', kwargs={'authenticator': authenticator})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(json_result['authenticator'], authenticator)

	def test_auth_delete_invalid(self):
		authenticator = "invalidauth"

		url = reverse('models:auth-delete', kwargs={'authenticator': authenticator})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])
