import urllib.request
import urllib.parse
import json
import requests

from django.shortcuts import render
from django.http import HttpResponseRedirect
import web.forms as forms

def create(request):
	if request.method == "GET":
		return __create_get(request)
	elif request.method == "POST":
		return __create_post(request)

def __create_get(request):
	form = forms.UserForm()
	return render(request, 'web/user-create.html', {'form': form})

def __create_post(request):
	form = forms.UserForm(request.POST)

	if form.is_valid():
		# Copy cleaned data items to data
		data = {}
		for field in form.cleaned_data:
			data[field] = form.cleaned_data[field]

		# Call exp service to create user
		url = 'http://exp-api:8000/exp/api/v1/auth/create_user'
		response = requests.post(url, data).json()

		# TODO: Failure behavior
		if not response['ok']:
			pass

		# TODO: Return the authenticator to the response redirect
		return HttpResponseRedirect('/')
	else:
		return render(request, 'web/user-create.html', {'form': form})

