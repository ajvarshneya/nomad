from django.test import TestCase, Client
from django.forms.models import model_to_dict
from models.models import *
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class ReviewApiTests(TestCase):
	fixtures = ['db']

	# Helper method to compare fields in a json result and a review model
	def compare_fields(self, json_result, review):
		for key in json_result:
			if key == "user":
				self.assertEqual(json_result["user"], review.user.id)
			elif key == "listing":
				self.assertEqual(json_result["listing"], review.listing.id)
			else:
				self.assertEqual(json_result[key], getattr(review, key))

	def test_review_index(self):
		response = self.client.get('/models/api/v1/reviews/')
		reviews = Review.objects.all()

		self.assertEqual(response.status_code, 200)

		# Get json data from response
		json_result = get_json_response(response)['result']

		# Check that all models were returned
		self.assertEqual(len(json_result), len(reviews))

	def test_review_detail_get_valid(self):
		review_id = 1
		review = Review.objects.get(pk=review_id)

		response = self.client.get('/models/api/v1/reviews/' + str(review_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# # Compare all result fields to those in the model
		self.compare_fields(json_result, review)

	def test_review_detail_get_invalid(self):
		review_id = 0

		response = self.client.get('/models/api/v1/reviews/' + str(review_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_review_detail_post_valid(self):
		review_id = 1
		review = Review.objects.get(pk=review_id)
		data = model_to_dict(review)
		data['title'] = "New title here"

		response = self.client.post('/models/api/v1/reviews/' + str(review_id) + '/', data)

		self.assertEqual(response.status_code, 200)

		# Get updated model
		review = Review.objects.get(pk=review_id)

		json_result = get_json_response(response)['result']

		# Compare all result fields to those in the model 
		self.compare_fields(json_result, review)

	def test_review_detail_post_invalid_id(self):
		review_id = 0

		# Get data for a review in the database
		review = Review.objects.all()[0]
		data = model_to_dict(review)
		data.pop('id', None)
		data['title'] = "New title here"

		response = self.client.post('/models/api/v1/reviews/' + str(review_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_review_detail_post_invalid_data(self):
		review_id = 1
		review = Review.objects.get(pk=review_id)
		data = model_to_dict(review)
		data.pop('title', None)

		response = self.client.post('/models/api/v1/reviews/' + str(review_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		self.assertEqual(json_response["ok"], False)
		errors = json_response["error"]
		for field in errors:
			self.assertIn("This field is required.", errors[field])

	def test_review_detail_delete_valid(self):
		review_id = 1
		response = self.client.delete('/models/api/v1/reviews/' + str(review_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(json_result['id'], str(review_id))

	def test_review_detail_delete_invalid(self):
		review_id = 0
		response = self.client.delete('/models/api/v1/reviews/' + str(review_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_review_create_valid(self):
		data = {
			"comment": "new comment text here",
			"title": "Relaxing Beach House",
			"user": 3,
			"rating": 4,
			"listing": 1,
		}
		response = self.client.post('/models/api/v1/reviews/create/', data)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# Get the new model
		review_id = json_result['id']
		review = Review.objects.get(pk=review_id)

		# Compare all result fields to those in the model
		self.compare_fields(json_result, review)

	def test_review_create_invalid(self):
		data = {
			"comment": "new comment text here",
			# "title": "Relaxing Beach House",
			"user": 3,
			# "rating": 4,
			"listing": 1,
		}
		response = self.client.post('/models/api/v1/reviews/create/', data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		self.assertEqual(json_response["ok"], False)
		errors = json_response["error"]
		for field in errors:
			self.assertIn("This field is required.", errors[field])