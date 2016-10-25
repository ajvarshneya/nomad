from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from models.models import *

def index(request):
	users = User.objects.all()

	user_dict_list = [__user_to_dict(user) for user in users]

	response = {
		"ok": True,
		"result": user_dict_list
	}

	return JsonResponse(response)

def auth(request):
	username = request.POST['username']
	password = request.POST['password']

	try:
		user = User.objects.get(username=username, password=password)
	except User.DoesNotExist:
		return JsonResponse({
			"ok" : False,
			"error": "User does not exist"
			})

	user_dict = __user_to_dict(user)

	response = {
		"ok": True,
		"result": user_dict
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
		"zipcode",
		"profile_image"
	]

	user_dict = __user_to_dict(user)

	truncated_user_dict = { k : user_dict[k] for k in user_dict if k in fields}

	response = {
		"ok": True,
		"result": truncated_user_dict
	}

	return JsonResponse(response)	

def __detail_post(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return JsonResponse({
				"ok": False,
				"error": "User does not exist"
			})

	# Include the current user instance in the UserForm
	# Note: Do this to prevent erros with created_at and updated_at
	user_form = UserForm(request.POST, instance=user)

	if not user_form.is_valid():
		return JsonResponse({
				"ok": False,
				"error": user_form.errors
			})

	# Do not commit the changes yet
	new_user = user_form.save(commit=False)

	# Set the user id to the one in the database and then save
	new_user.id = int(user_id)
	new_user.save()

	user_dict = __user_to_dict(new_user)

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
				"error": "User does not exist"
			})

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

	user_dict = __user_to_dict(new_user)

	response = {
		"ok": True,
		"result": user_dict,
	}

	return JsonResponse(response)

def __user_to_dict(user):
	user_dict = model_to_dict(user)

	# Get profile image for the user and remove redundant user id info on the image
	if hasattr(user, 'profile_image'):
		user_dict['profile_image'] = model_to_dict(user.profile_image)
		user_dict['profile_image'].pop('user', None)

	return user_dict
