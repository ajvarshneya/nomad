from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from api.models import *

def index(request):
	return JsonResponse({"ok": False})

def detail(request, review_id):
	if request.method == "GET":
		return __detail_get(request, review_id)
	elif request.method == "POST":
		return __detail_post(request, review_id)
	elif request.method == "DELETE":
		return __detail_delete(request, review_id)

def __detail_get(request, review_id):
	return JsonResponse({"ok": False})

def __detail_post(request, review_id):
	return JsonResponse({"ok": False})

def __detail_delete(request, review_id):
	return JsonResponse({"ok": False})

def create(request):
	return JsonResponse({"ok": False})