import urllib.request
import urllib.parse
import json

from django.http import HttpResponse, Http404
from django.template import loader

def index(request):
	template = loader.get_template('web/listings.html')

	models_request = urllib.request.Request('http://exp-api:8000/exp/api/v1/listings')
	json_response = urllib.request.urlopen(models_request).read().decode('utf-8')
	response = json.loads(json_response)

	if "ok" in response and response["ok"]:
		context = {"listings" : response["result"]}
		return HttpResponse(template.render(context, request))
	else:
		raise Http404(response)
	
def detail(request, listing_id):
	template = loader.get_template('web/listing-detail.html')

	exp_request = urllib.request.Request('http://exp-api:8000/exp/api/v1/listings/{}/'.format(listing_id))
	json_response = urllib.request.urlopen(exp_request).read().decode('utf-8')
	response = json.loads(json_response)

	if "ok" in response and response["ok"]:
		context = {"listing": response["result"]}
		return HttpResponse(template.render(context, request))
	else:
		raise Http404(response)
