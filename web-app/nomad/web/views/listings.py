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
	return HttpResponse("listing_id " + listing_id)