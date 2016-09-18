from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from api.models import *

def index(request):
	users = User.objects.all()

	user_dict_list = [model_to_dict(user) for user in users]

	response = {
		"ok": True,
		"result": user_dict_list
	}

	return JsonResponse(response)

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
		return JsonResponse({
			"ok" : False,
			"error": "User does not exist"
			})
	
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

	response = {
		"ok": True,
		"result": truncated_user_dict
	}

	return JsonResponse(response)

def __detail_post(request, user_id):
	user_form = UserForm(request.POST)

	if not user_form.is_valid():
		return JsonResponse({
			"ok": False,
			"error": user_form.errors
			})

	# Do not commit the changes yet
	new_user = user_form.save(commit=False)

	# Set the user id to the one in the database and then save
	new_user.id = user_id
	new_user.save()

	user_dict = model_to_dict(new_user)

	response = {
		"ok": True,
		"result": user_dict,
	}

	return JsonResponse(response)

def __detail_delete(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return JsonResponse({
			"ok": False,
			"error": "User does not exist"})

	user.delete()

	response = {
		"ok": True,
		"result": {
			"id": user_id
		}
	}

	return JsonResponse(response)

def create(request):
	user_form = UserForm(request.POST)

	if not user_form.is_valid():
		return JsonResponse({
			"ok": False,
			"error": user_form.errors
			})

	new_user = user_form.save()

	user_dict = model_to_dict(new_user)

	response = {
		"ok": True,
		"result": user_dict,
	}

	return JsonResponse(response)

