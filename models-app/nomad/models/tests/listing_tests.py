from django.test import TestCase, Client
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from models.models import *
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class ListingApiTests(TestCase):
	fixtures = ['db']

	# Helper method to compare fields in a json result and a listing model
	def compare_fields(self, json_result, listing):
		for key in json_result:
			# Handle special fields explicitly
			if key == "images":
				url_set = map(lambda image: image.url_full, listing.images.all())
				for image in json_result["images"]:
					self.assertIn(image["url_full"], url_set)
			elif key == "user":
				self.assertEqual(json_result[key], listing.user.id)
			elif key == "baths":
				self.assertEqual(json_result[key], str(listing.baths))
			elif key == "created_at" or key == "updated_at":
				# Skip created_at and updated_at fields
				continue
			else:
				self.assertEqual(json_result[key], getattr(listing, key))

	def test_listing_index(self):
		url = reverse('models:listings-index')
		response = self.client.get(url)
		listings = Listing.objects.all()

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(len(json_result), len(listings))

	def test_listing_detail_get_valid(self):
		listing_id = 1
		listing = Listing.objects.get(pk=listing_id)

		url = reverse('models:listings-detail', kwargs={'listing_id': listing_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# Compare all result fields to those in the model
		self.compare_fields(json_result, listing)

	def test_listing_detail_get_invalid(self):
		listing_id = 0

		url = reverse('models:listings-detail', kwargs={'listing_id': listing_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_listing_detail_post_valid(self):
		listing_id = 1
		listing = Listing.objects.get(pk=listing_id)
		data = model_to_dict(listing)
		data['title'] = "New title here"

		url = reverse('models:listings-detail', kwargs={'listing_id': listing_id})
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		# Get updated model
		listing = Listing.objects.get(pk=listing_id)

		json_result = get_json_response(response)['result']

		# Compare all result fields to those in the model 
		self.compare_fields(json_result, listing)

	def test_listing_detail_post_invalid_id(self):
		listing_id = 0

		# Get data for a listing in the database
		listing = Listing.objects.all()[0]
		data = model_to_dict(listing)
		data.pop('id', None)
		data['title'] = "New title here"

		url = reverse('models:listings-detail', kwargs={'listing_id': listing_id})
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_listing_detail_post_invalid_data(self):
		listing_id = 1
		listing = Listing.objects.get(pk=listing_id)
		data = model_to_dict(listing)
		data.pop('title', None)

		url = reverse('models:listings-detail', kwargs={'listing_id': listing_id})
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and form error message
		self.assertEqual(json_response["ok"], False)
		errors = json_response["error"]
		for field in errors:
			self.assertIn("This field is required.", errors[field])

	def test_listing_detail_delete_valid(self):
		listing_id = 1
		url = reverse('models:listings-detail', kwargs={'listing_id': listing_id})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(json_result['id'], str(listing_id))

	def test_listing_detail_delete_invalid(self):
		listing_id = 0
		url = reverse('models:listings-detail', kwargs={'listing_id': listing_id})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_listing_create_valid(self):
		data = {
			"title": "Relaxing Beach House",
			"country": "US",
			"zipcode": "67890",
			"beds": "4",
			"city": "beach city",
			"baths": "4.5",
			"street": "beach street",
			"user": "1",
			"price": "250",
		}
		url = reverse('models:listings-create')
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# Get the new user model
		listing_id = json_result['id']
		listing = Listing.objects.get(pk=listing_id)

		# Compare all result fields to those in the model
		self.compare_fields(json_result, listing)

	def test_listing_create_invalid(self):
		data = {
			# "title": "Relaxing Beach House",
			"country": "US",
			"zipcode": "67890",
			"beds": "4",
			# "city": "beach city",
			"baths": "4.5",
			"street": "beach street",
			"user": "1",
			# "price": "250",
		}
		url = reverse('models:listings-create')
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and form error message
		self.assertEqual(json_response["ok"], False)
		errors = json_response["error"]
		for field in errors:
			self.assertIn("This field is required.", errors[field])
