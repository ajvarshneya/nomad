from django.core import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict
from api.models import *

def detail(request, user_id):
	if request.method == "GET":
		return __detail_get(request, user_id)
	elif request.method == "PUT":
		return __detail_put(request, user_id)
	elif request.method == "DELETE":
		return __detail_delete(request, user_id)
		
def __detail_get(request, user_id):
	user = User.objects.get(pk=user_id)
		
	if not user:
		return JsonResponse({"ok" : False})	
	
	fields = [
		"first_name", 
		"last_name", 
		"email", 
		"username", 
		"street", 
		"city", 
		"country", 
		"zipcode"
	]

	user_dict = model_to_dict(user)

	truncated_user_dict = { k : user_dict[k] for k in user_dict if k in fields}

	result = {
		'ok': True,
		'result': truncated_user_dict
	}

	return JsonResponse(result, safe=False)

def __detail_put(request, user_id):
	pass

def __detail_delete(request, user_id):
	pass

def create(request):
	return JsonResponse({"ok": False})


