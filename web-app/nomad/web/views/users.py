import urllib.request
import urllib.parse
import json

from django.shortcuts import render
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
	pass

