from django.core import serializers
from django.http import JsonResponse
from api.models import *

def detail(request, user_id):
	if request.method == "GET":
		return __detail_get(request, user_id)
	elif request.method == "PUT":
		return __detail_put(request, user_id)
	elif request.method == "DELETE":
		return __detail_delete(request, user_id)
		
def __detail_get(request, user_id):
	user = User.objects.filter(pk=user_id)
		
	if not user:
		return JsonResponse({"ok" : False})	
	
	data = user.values("first_name", 
					 "last_name", 
					 "email", 
					 "username", 
					 "street", 
					 "city", 
					 "country", 
					 "zipcode")[0]

	result = {
		'ok': True,
		'result': data
	}

	return JsonResponse(result, safe=False)

def __detail_put(request, user_id):
	pass

def __detail_delete(request, user_id):
	pass

def create(request):
	return JsonResponse({"ok": False})


