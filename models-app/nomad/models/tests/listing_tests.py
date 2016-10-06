from django.test import TestCase, Client
from django.forms.models import model_to_dict
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
			else:
				self.assertEqual(json_result[key], getattr(listing, key))

	def test_listing_index(self):
		response = self.client.get('/models/api/v1/listings/')
		listings = Listing.objects.all()

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(len(json_result), len(listings))

	def test_listing_detail_get_valid(self):
		listing_id = 1
		listing = Listing.objects.get(pk=listing_id)

		response = self.client.get('/models/api/v1/listings/' + str(listing_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# # Compare all result fields to those in the model
		self.compare_fields(json_result, listing)

	def test_listing_detail_get_invalid(self):
		listing_id = 0

		response = self.client.get('/models/api/v1/listings/' + str(listing_id) + '/')

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

		response = self.client.post('/models/api/v1/listings/' + str(listing_id) + '/', data)

		self.assertEqual(response.status_code, 200)

		# Get updated model
		listing = Listing.objects.get(pk=listing_id)

		json_result = get_json_response(response)['result']

		# Compare all result fields to those in the model 
		self.compare_fields(json_result, listing)

	def test_listing_detail_post_invalid(self):
		listing_id = 0

		# Get data for a listing in the database
		listing = Listing.objects.all()[0]
		data = model_to_dict(listing)
		data.pop('id', None)
		data['title'] = "New title here"

		response = self.client.post('/models/api/v1/listings/' + str(listing_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_listing_detail_delete_valid(self):
		listing_id = 1
		response = self.client.delete('/models/api/v1/listings/' + str(listing_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(json_result['id'], str(listing_id))

	def test_listing_detail_delete_invalid(self):
		listing_id = 0
		response = self.client.delete('/models/api/v1/listings/' + str(listing_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_listing_create(self):
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

		response = self.client.post('/models/api/v1/listings/create/', data)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# Get the new user model
		listing_id = json_result['id']
		listing = Listing.objects.get(pk=listing_id)

		# Compare all result fields to those in the model
		self.compare_fields(json_result, listing)