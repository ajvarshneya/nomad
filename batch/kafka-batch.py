from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json
import sys

# Create a new KafkaConsumer
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'], api_version='0.9')

while True:
	added_item = False
	for message in consumer:
		# Decode the json from the message
		listing = json.loads((message.value).decode('utf-8'))

		# Add the listing from the message to elasticsearch
		es.index(index='listing-index', doc_type='listing')

	# If item(s) added, update search index
	if added_item:
		es.indices.refresh(index='listing-index')
