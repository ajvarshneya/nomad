import urllib.request
import urllib.parse
import json
import requests
import time
import sys

from elasticsearch import Elasticsearch

# --------------------------------------------------------------------------------
# Script to load data from database directly into ElasticSearch.
# Note: This is only run when the container starts to add the data from fixtures
#	and the database into the search index.
# --------------------------------------------------------------------------------

# Wait for other containers
# Note: Use a large amount of time to allow for migrations and ES config
time.sleep(45)
print("Loading DB data into search index...")
sys.stdout.flush()

# Listings model API call
index_request = urllib.request.Request('http://models-api:8000/models/api/v1/listings/')
json_index_response = urllib.request.urlopen(index_request).read().decode('utf-8')
index_response = json.loads(json_index_response)

# Manually add the items to ElasticSearch
es = Elasticsearch(['es'])
for listing in index_response["result"]:
	es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
es.indices.refresh(index='listing_index')
print("Done adding listings from DB to index")