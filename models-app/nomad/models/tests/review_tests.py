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
			self.assertEqual(json_result[key], getattr(review, key))

	def test_review_index(self):
		pass

	def test_review_detail_get_valid(self):
		pass

	def test_review_detail_get_invalid(self):
		pass

	def test_review_detail_post_valid(self):
		pass

	def test_review_detail_post_invalid(self):
		pass

	def test_review_detail_delete_valid(self):
		pass

	def test_review_detail_delete_invalid(self):
		pass

	def test_review_create(self):
		pass