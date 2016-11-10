from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from datetime import datetime
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from threading import Thread
import json
import time

def get_json_response(json_response):
	return json.loads(json_response.content.decode('utf-8'))

class SearchExpTests(TestCase):
	def test_listing_kafka(self):
		"""
		Check that creating a listing adds the data to Kafka
		"""
		# Log in
		url = reverse("exp:auth-login")
		data = {
			"username" : "ironman",
			"password" : "password"
		}
		response = self.client.post(url, data)
		json_response = get_json_response(response)

		# Data to make new listing
		url = reverse('exp:listings-create')
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
		data['auth'] = json_response['result']['authenticator']

		# Create new KafkaConsumer to subscribe to listing events
		# Set the timeout to 1000 to stop listening for messages
		consumer = KafkaConsumer('new-listings-topic',
			group_id='listing-indexer',
			bootstrap_servers=['kafka:9092'])

		# Simple method to run in the thread
		def kafka_consume(consumer, results):
			message = next(consumer)
			results.append(message)

		# Start thread to wait for response
		kafka_results = []
		thread = Thread(target=kafka_consume, args=(consumer, kafka_results))
		thread.start()

		# Send url request (causes Kafka to publish listing event)
		response = self.client.post(url, data)
		result = get_json_response(response)['result']
		listing_id = result['id']

		# Wait for a bit so the consumer has time to receive the message
		time.sleep(1)

		# Check that a message was received
		self.assertEqual(len(kafka_results), 1)

		# Decode the json from the message
		message = kafka_results[0]
		listing = json.loads((message.value).decode('utf-8'))

		# Check all data fields except auth
		del data['auth']
		for key in data:
			self.assertEqual(data[key], str(listing[key]))

	def test_search_results(self):
		"""
		Check that search returns results
		"""
		url = reverse('exp:listings-search')
		query = "FR"
		response = self.client.get(url, {'query': query})
		self.assertEqual(response.status_code, 200)

		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertTrue(json_response["result"])

		json_results = json_response["result"]

		# Perform query directly on ES
		es = Elasticsearch(['es'])
		query_body = {
			'query': {
				'query_string': {
					'query': query
				},
			},
			'size': 10
		}
		es_results = es.search(index='listing_index', body=query_body)['hits']['hits']
		es_results = [result['_source'] for result in es_results]

		# Check that the same number of results are returned
		self.assertEqual(len(json_results), len(es_results))

		# Check that the results are in the same order
		for i in range(len(json_results)):
			self.assertEqual(json_results[i]['title'], es_results[i]['title'])
			self.assertEqual(json_results[i]['street'], es_results[i]['street'])
			self.assertEqual(json_results[i]['created_at'], es_results[i]['created_at'])

	def test_search_empty(self):
		"""
		Check search with empty query
		"""
		url = reverse('exp:listings-search')
		query = ""
		response = self.client.get(url, {'query': query})
		self.assertEqual(response.status_code, 200)

		# Check that the response has an empty result
		json_response = get_json_response(response)
		self.assertTrue(json_response["ok"])
		self.assertFalse(json_response["result"])
