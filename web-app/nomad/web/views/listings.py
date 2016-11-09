import urllib.request
import urllib.parse
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse as reverse
from django.template import loader

import web.forms as forms

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

def create(request):
	# User not logged in, so redirect to login page
	auth = request.COOKIES.get('auth')
	if not auth:
		return HttpResponseRedirect(get_next_url('web:auth-login', 'web:listings-create'))

	if request.method == "GET":
		form = forms.ListingForm()
		return render(request, 'web/listing-create.html', {'form':form})

	elif request.method == "POST":
		form = forms.ListingForm(request.POST)

		# Ensure the form is valid
		if not form.is_valid():
			return render(request, 'web/listing-create.html', {'form':form})

		# Copy cleaned data items to data
		data = {}
		for field in form.cleaned_data:
			data[field] = form.cleaned_data[field]
		data['auth'] = auth

		# Call exp service to create listing
		url = 'http://exp-api:8000/exp/api/v1/listings/create/'
		response = requests.post(url, data)
		json_response = response.json()

		# Check response to see if auth was valid
		# If auth not valid, redirect to login with next=listings-create
		if not json_response["ok"]:
			if json_response["error_type"] == 'auth':
				return HttpResponseRedirect(get_next_url('web:auth-login', 'web:listings-create'))

		# No errors, so redirect to listing detail page
		listing_id = json_response['result']['id']
		return redirect('web:listings-detail', listing_id=listing_id)

def search(request):
	template = loader.get_template('web/search-results.html')

	query = request.GET['query']
	url = 'http://exp-api:8000/exp/api/v1/listings/search?query={}'.format(query)
	response = requests.get(url)
	json_response = response.json()

	if "ok" in json_response and json_response["ok"]:
		context = {"listings" : json_response["result"]}
		return HttpResponse(template.render(context, request))
	else:
		raise Http404(json_response)

def get_next_url(base, next):
	return "{}?next={}".format(reverse(base), reverse(next))
