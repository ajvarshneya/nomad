from django.test import TestCase, Client
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from models.models import *
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class TagApiTests(TestCase):
	fixtures = ['db']

	# Helper method to compare fields in a json result and a tag model
	def compare_fields(self, json_result, tag):
		for key in json_result:
			if key == "listings":
				listing_id_set = set(map(lambda listing: listing.id, tag.listings.all()))
				for listing_id in json_result["listings"]:
					self.assertIn(listing_id, listing_id_set)
			else:
				self.assertEqual(json_result[key], getattr(tag, key))

	def test_tag_index(self):
		url = reverse('models:tags-index')
		response = self.client.get(url)
		tags = Tag.objects.all()

		self.assertEqual(response.status_code, 200)

		# Get json data from response
		json_result = get_json_response(response)['result']

		# Check that all models were returned
		self.assertEqual(len(json_result), len(tags))


	def test_tag_detail_get_valid(self):
		tag_id = 1
		tag = Tag.objects.get(pk=tag_id)

		url = reverse('models:tags-detail', kwargs={"tag_id": tag_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# # Compare all result fields to those in the model
		self.compare_fields(json_result, tag)

	def test_tag_detail_get_invalid(self):
		tag_id = 0

		url = reverse('models:tags-detail', kwargs={"tag_id": tag_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_tag_detail_post_valid(self):
		tag_id = 1
		tag = Tag.objects.get(pk=tag_id)
		data = model_to_dict(tag)
		data['text'] = "New text here"

		url = reverse('models:tags-detail', kwargs={"tag_id": tag_id})
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		# Get updated model
		tag = Tag.objects.get(pk=tag_id)

		json_result = get_json_response(response)['result']

		# Compare all result fields to those in the model 
		self.compare_fields(json_result, tag)

	def test_tag_detail_post_invalid_id(self):
		tag_id = 0

		# Get data for a tag in the database
		tag = Tag.objects.all()[0]
		data = model_to_dict(tag)
		data.pop('id', None)
		data['text'] = "New title here"

		url = reverse('models:tags-detail', kwargs={"tag_id": tag_id})
		response = self.client.post(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

	def test_tag_detail_post_invalid_data(self):
		tag_id = 1
		tag = Tag.objects.get(pk=tag_id)
		data = model_to_dict(tag)
		data.pop('text', None)

		url = reverse('models:tags-detail', kwargs={"tag_id": tag_id})
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and form error message
		self.assertEqual(json_response["ok"], False)
		errors = json_response["error"]
		for field in errors:
			self.assertIn("This field is required.", errors[field])

	def test_tag_detail_delete_valid(self):
		tag_id = 1
		url = reverse('models:tags-detail', kwargs={"tag_id": tag_id})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(json_result['id'], str(tag_id))

	def test_tag_detail_delete_invalid(self):
		tag_id = 0
		url = reverse('models:tags-detail', kwargs={"tag_id": tag_id})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_tag_create_valid(self):
		data = {
			"text": "suburban",
			"listings": 1,
		}
		url = reverse('models:tags-create')
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# Get the new model
		tag_id = json_result['id']
		tag = Tag.objects.get(pk=tag_id)

		# Compare all result fields to those in the model
		self.compare_fields(json_result, tag)

	def test_tag_create_invalid(self):
		data = {
			# "text": "suburban",
			"listings": 1,
		}
		url = reverse('models:tags-create')
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and form error message
		self.assertEqual(json_response["ok"], False)
		errors = json_response["error"]
		for field in errors:
			self.assertIn("This field is required.", errors[field])
