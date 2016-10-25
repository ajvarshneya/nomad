import urllib.request
import urllib.parse
import json

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

	# TODO: Check login via EXP service
	# If not valid, render login page with errors

	# Set authenticator in request cookie and redirect back to next
	# TODO: Get authenticator from EXP response
	http_response = HttpResponseRedirect(next)
	http_response.set_cookie('auth', "TODO: authenticator here")
	return http_response

def logout(request):
	# TODO: Delete authenticator via EXP service

	# Clear authenticator from cookies
	next = request.GET.get('next') or reverse('web:index')
	http_response = HttpResponseRedirect(next)
	http_response.delete_cookie('auth')
	return http_response
