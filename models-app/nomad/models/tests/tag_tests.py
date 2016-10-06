from django.test import TestCase, Client
from django.forms.models import model_to_dict
from models.models import *
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class TagApiTests(TestCase):
	fixtures = ['db']

	# Helper method to compare fields in a json result and a tag model
	def compare_fields(self, json_result, tag):
		for key in json_result:
			self.assertEqual(json_result[key], getattr(tag, key))

	def test_tag_index(self):
		pass

	def test_tag_detail_get_valid(self):
		pass

	def test_tag_detail_get_invalid(self):
		pass

	def test_tag_detail_post_valid(self):
		pass

	def test_tag_detail_post_invalid(self):
		pass

	def test_tag_detail_delete_valid(self):
		pass

	def test_tag_detail_delete_invalid(self):
		pass

	def test_tag_create(self):
		pass