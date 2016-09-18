from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from api.models import *

def detail(request, user_id):
	if request.method == "GET":
		return __detail_get(request, user_id)
	elif request.method == "POST":
		return __detail_post(request, user_id)
	elif request.method == "DELETE":
		return __detail_delete(request, user_id)
		
def __detail_get(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
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
		"ok": True,
		"result": truncated_user_dict
	}

	return JsonResponse(result, safe=False)

def __detail_post(request, user_id):
	user_form = UserForm(request.POST)

	if not user_form.is_valid():
		return JsonResponse({"ok": False})

	# Do not commit the changes yet
	new_user = user_form.save(commit=False)

	# Set the user id to the one in the database and then save
	new_user.id = user_id
	new_user.save()

	user_dict = model_to_dict(new_user)

	result = {
		"ok": True,
		"result": user_dict,
	}

	return JsonResponse(result)

def __detail_delete(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return JsonResponse({"ok": False})

	user.delete()

	result = {
		"ok": True,
		"result": {
			"id": user_id
		}
	}

	return JsonResponse(result)

def create(request):
	user_form = UserForm(request.POST)

	if not user_form.is_valid():
		return JsonResponse({"ok": False})

	new_user = user_form.save()

	user_dict = model_to_dict(new_user)

	result = {
		"ok": True,
		"result": user_dict,
	}

	return JsonResponse(result)


