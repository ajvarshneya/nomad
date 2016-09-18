from django.core import serializers
from django.http import JsonResponse
from api.models import *

def detail(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return JsonResponse({"ok" : False})	
	
	fields_to_get = ("first_name", 
					 "last_name", 
					 "email", 
					 "username", 
					 "street", 
					 "city", 
					 "country", 
					 "zipcode")

	data = serializers.serialize('json', [user], fields=fields_to_get)

	return JsonResponse(data)





