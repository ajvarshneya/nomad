from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

# Create your tests here.
class HomeViewTests(TestCase):
	def test_index_view_valid(self):
		"""
		Check for valid response
		"""
		response = self.client.get(reverse("web:index"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Nomad")
		self.assertContains(response, "Not All Those Who Wander Are Lost")

class ListingViewTests(TestCase):
	def test_index_view_valid(self):
		"""
		Check for valid response with 1+ views
		"""
		response = self.client.get(reverse("web:listings-index"))
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, "No listings found")

	def test_detail_view_valid(self):
		"""
		Check for valid response with valid listing id
		"""
		url = reverse("web:listings-detail", kwargs={'listing_id': 1})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_detail_view_invalid(self):
		"""
		Check for 404 page with invalid listing id
		"""
		# listing id can never be 0, so use that as the invalid id
		url = reverse("web:listings-detail", kwargs={'listing_id': 0})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
