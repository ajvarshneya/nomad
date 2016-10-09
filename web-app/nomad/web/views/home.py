import urllib.request
import urllib.parse
import json

from django.http import HttpResponse
from django.template import loader

def index(request):
	template = loader.get_template('web/index.html')

	context = {}

	# Get most recent listings
	most_recent_listings = urllib.request.Request('http://exp-api:8000/exp/api/v1/listings/most_recent/?limit=3')
	json_response = urllib.request.urlopen(most_recent_listings).read().decode('utf-8')
	response = json.loads(json_response)

	if "ok" in response and response["ok"]:
		context['most_recent_listings'] = response["result"]
	else:
		raise Http404(response)


	# TODO: Get most popular listings

	return HttpResponse(template.render(context, request))


	
