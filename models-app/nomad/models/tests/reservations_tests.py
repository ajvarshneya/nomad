from django.test import TestCase, Client
from django.forms.models import model_to_dict
from models.models import *
import json

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class ReservationsApitTests(TestCase):
	fixtures = ['db']

	def compare_fields(self, json_result, reservation):
		for key in json_result:
			# Handle special fields explicitly
			if key == "start_date":
				self.assertEqual(json_result[key],
					str(reservation.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")))
			elif key == "end_date":
				self.assertEqual(json_result[key],
					str(reservation.end_date.strftime("%Y-%m-%dT%H:%M:%SZ")))
			elif key == "listing":
				self.assertEqual(json_result[key], reservation.listing.id)
			elif key == "user":
				self.assertEqual(json_result[key], reservation.user.id)
			else:
				self.assertEqual(json_result[key], getattr(reservation, key))

	def test_reservation_index(self):
		response = self.client.get('/models/api/v1/users/')
		reservations = Reservation.objects.all()

		self.assertEqual(response.status_code, 200)

		# Check that all reservations were returned
		json_result = get_json_response(response)['result']
		self.assertEqual(len(json_result), len(reservations))

	def test_reservation_detail_get_valid(self):
		reservation_id = 1
		reservation = Reservation.objects.get(pk=reservation_id)

		response = self.client.get('/models/api/v1/reservations/' + str(reservation_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# # Compare all result fields to those in the model
		self.compare_fields(json_result, reservation)

	def test_reservation_detail_get_invalid(self):
		reservation_id = 0

		response = self.client.get('/models/api/v1/reservations/' + str(reservation_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_reservation_detail_post_valid(self):
		reservation_id = 1
		reservation = Reservation.objects.get(pk=reservation_id)
		data = model_to_dict(reservation)
		data['start_date'] = "2016-09-19 12:00"
		data['end_date'] = "2016-09-26 12:00"

		response = self.client.post('/models/api/v1/reservations/' + str(reservation_id) + '/', data)

		self.assertEqual(response.status_code, 200)

		# Get updated model
		reservation = Reservation.objects.get(pk=reservation_id)

		json_result = get_json_response(response)['result']

		self.compare_fields(json_result, reservation)

	def test_reservation_detail_post_invalid(self):
		reservation_id = 0

		# Get data for a reservation
		reservation = Reservation.objects.all()[0]
		data = model_to_dict(reservation)
		data.pop('id', None)
		data['start_date'] = "2016-09-19 12:00"
		data['end_date'] = "2016-09-26 12:00"

		response = self.client.post('/models/api/v1/reservations/' + str(reservation_id) + '/', data)

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_reservation_detail_delete_valid(self):
		reservation_id = 1
		response = self.client.delete('/models/api/v1/reservations/' + str(reservation_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']
		self.assertEqual(json_result['id'], str(reservation_id))

	def test_reservation_detail_delete_invalid(self):
		reservation_id = 0
		response = self.client.delete('/models/api/v1/reservations/' + str(reservation_id) + '/')

		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)

		# Check for ok: False and DNE error message
		self.assertEqual(json_response["ok"], False)
		self.assertIn("does not exist", json_response["error"])

	def test_reservation_create(self):
		data = {
			"is_available": "false",
			"start_date": "2016-09-19 12:00",
			"end_date": "2016-09-26 12:00",
			"listing": 4,
			"user": 1,
		}
		response = self.client.post('/models/api/v1/reservations/create/', data)

		self.assertEqual(response.status_code, 200)

		json_result = get_json_response(response)['result']

		# Get the new reservation model
		reservation_id = json_result['id']
		reservation = Reservation.objects.get(pk=reservation_id)

		# Compare all result fields to those in the model
		self.compare_fields(json_result, reservation)
