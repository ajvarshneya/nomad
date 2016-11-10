from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from datetime import datetime
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class ListingsExpTests(TestCase):
	def test_index_valid(self):
		"""
		Check for valid response
		"""
		url = reverse("exp:listings-index")
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check that the status is ok and the result is not empty
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

	def test_detail_valid(self):
		"""
		Check for detail when fetching a listing with a valid id
		"""
		url = reverse("exp:listings-detail", kwargs={'listing_id':1, })
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

		# Check that the json result has the desired fields
		json_result = json_response["result"]
		fields_to_check = [
			"title",
			"price",
			"user",
		]
		for field in fields_to_check:
			self.assertTrue(json_result[field])

		# Check that the user field has been included inline
		# Every user has a non-empty email, so just check for the email field
		self.assertIn("email", json_result["user"])
		self.assertTrue(json_result["user"]["email"])

	def test_detail_invalid_id(self):
		"""
		Check for error response when fetching a listing with an invalid id
		"""
		url = reverse("exp:listings-detail", kwargs={'listing_id':0, })
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		json_response = get_json_response(response)
		self.assertFalse(json_response["ok"])
		self.assertFalse(json_response["result"])

	def test_most_recent(self):
		"""
		Check that the listings are ordered from most to least recent
		"""
		url = reverse("exp:listings-most-recent")
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

		json_result = json_response["result"]

		# Compare the date of each listing to the one after it
		for i in range(len(json_result)-1):
			cur_date = datetime.strptime(json_result[i]["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
			next_date = datetime.strptime(json_result[i+1]["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
			self.assertTrue(cur_date >= next_date)

	def test_most_recent_limit(self):
		"""
		Check that the limit GET param limits the number of responses
		"""
		limit = 2
		url = reverse("exp:listings-most-recent")
		response = self.client.get(url, {'limit': limit})
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

		json_result = json_response["result"]
		self.assertEqual(len(json_result), limit)

	def test_most_popular(self):
		"""
		Check that the listings are ordered from most to least popular
		"""
		url = reverse("exp:listings-most-popular")
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])
		
		json_result = json_response["result"]

		# Compare the rating of each listing to the one after it 
		for i in range(len(json_result)-1):
			cur_rating = json_result[i]["rating"]
			next_rating = json_result[i+1]["rating"]
			self.assertTrue(cur_rating >= next_rating)

	def test_most_popular_limit(self):
		"""
		Check that the limit GET param limits the number of responses
		"""
		limit = 2
		url = reverse("exp:listings-most-popular")
		response = self.client.get(url, {'limit': limit})
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

		json_result = json_response["result"]
		self.assertEqual(len(json_result), limit)
