import urllib.request
import urllib.parse
import json
import requests

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse as reverse
import web.forms as forms

def login(request):
	if request.method == "GET":
		return __login_get(request)
	elif request.method == "POST":
		return __login_post(request)

def __login_get(request):
	next = request.GET.get('next') or reverse('web:index')
	login_form = forms.LoginForm(initial={'next': next})
	context = {
		'form': login_form,
	}
	return render(request, 'web/login.html', context)

def __login_post(request):
	login_form = forms.LoginForm(request.POST)

	# Form not valid, so return error messages
	if not login_form.is_valid():
		return render(request, 'web/login.html', {'form': login_form})

	# Get cleaned username and password
	username = login_form.cleaned_data['username']
	password = login_form.cleaned_data['password']
	next = login_form.cleaned_data['next'] or reverse('web:index')

	# Check login via exp service
	url = 'http://exp-api:8000/exp/api/v1/auth/login'
	data = {
		'username': username,
		'password': password,
	}
	response = requests.post(url, data)
	json_response = response.json()

	# If not valid, render login page with errors
	if not json_response["ok"]:
		context = {
			'form': login_form,
			'error': 'Invalid username or password',
		}
		return render(request, 'web/login.html', context)

	# Set authenticator in request cookie and redirect back to next
	http_response = HttpResponseRedirect(next)
	http_response.set_cookie('auth', json_response['result']['authenticator'])
	return http_response

def logout(request):
	# Delete authenticator via exp service
	url = 'http://exp-api:8000/exp/api/v1/auth/logout'
	authenticator = request.COOKIES.get('auth')
	data = {
		'authenticator': authenticator
	}
	response = requests.post(url, data)
	json_response = response.json()

	# TODO: Add effective way to alert user that logout failed

	# Clear authenticator from cookies
	next = request.GET.get('next') or reverse('web:index')
	http_response = HttpResponseRedirect(next)
	http_response.delete_cookie('auth')
	return http_response