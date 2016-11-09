from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
import json
import sys
import time

# Create a new KafkaConsumer
consumer = None
while not consumer:
	try:
		consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
	except NodeNotReadyError:
		time.sleep(30)

es = Elasticsearch(['es'])

while True:
	added_item = False
	for message in consumer:
		# Decode the json from the message
		listing = json.loads((message.value).decode('utf-8'))

		# Add the listing from the message to elasticsearch
		es.index(index='listing-index', doc_type='listing', id=listing['id'], body=listing)

	# If item(s) added, update search index
	if added_item:
		es.indices.refresh(index='listing-index')
