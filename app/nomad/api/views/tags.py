from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from api.models import *

def index(request):
	return JsonResponse({"ok": False})

def detail(request, tag_id):
	if request.method == "GET":
		return __detail_get(request, tag_id)
	elif request.method == "POST":
		return __detail_post(request, tag_id)
	elif request.method == "DELETE":
		return __detail_delete(request, tag_id)

def __detail_get(request, tag_id):
	return JsonResponse({"ok": False})

def __detail_post(request, tag_id):
	return JsonResponse({"ok": False})

def __detail_delete(request, tag_id):
	return JsonResponse({"ok": False})

def create(request):
	return JsonResponse({"ok": False})