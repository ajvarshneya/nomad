import urllib.request
import urllib.parse
import json

from django.http import HttpResponse
from django.template import loader

def index(request):
	template = loader.get_template('web/listings.html')

	models_request = urllib.request.Request('http://exp-api:8000/exp/api/v1/listings')
	json_response = urllib.request.urlopen(models_request).read().decode('utf-8')
	response = json.loads(json_response)

	if response["ok"]:
		context = {"listings" : response["result"]}
		return HttpResponse(template.render(context, request))
	
def detail(request, listing_id):
	template = loader.get_template('web/listing-detail.html')

	# Placeholder response data since exp layer not built out yet
	response = {
		"ok": True,
		"result": {
			"zipcode": "12345",
			"title": "Beach House",
			"id": 1,
			"street": "beach street",
			"baths": "4.5",
			"user": {
				"zipcode": "10118",
				"email": "ironman@marvel.com",
				"username": "ironman",
				"last_name": "Stark",
				"first_name": "Tony",
				"street": "350 5th Ave",
				"city": "New York",
				"country": "US"
			},
			"city": "beach city",
			"country": "US",
			"beds": 4,
			"reviews": [
			],
			"reservations": [
				{
					"start_date": "2016-09-17T10:00:00Z",
					"id": 4,
					"user": 3,
					"listing": 1,
					"is_available": False,
					"end_date": "2016-09-21T19:00:00Z"
				}
			]
		}
	}

	if response["ok"]:
		context = {"listing": response["result"]}
		return HttpResponse(template.render(context, request))
