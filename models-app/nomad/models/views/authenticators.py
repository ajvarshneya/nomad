from django.http import JsonResponse
from django.forms.models import model_to_dict
from models.models import *

import os
import hmac
import nomad.settings as settings

def check(request, authenticator):
	try:
		auth_model = Authenticator.objects.get(pk=authenticator)
	except Authenticator.DoesNotExist:
		# Authenticator no in DB, so return ok = False
		return JsonResponse({
				"ok": False,
				"error": "Authenticator does not exist"
			})

	# Authenticator exists, so return ok = True
	response = {
		"ok": True,
		"result": model_to_dict(auth_model)
	}

	return JsonResponse(response)

def create(request, user_id):
	# Check if auth_model already exists for the user	
	auth_models = Authenticator.objects.filter(user_id=user_id)

	if auth_models:
		return JsonResponse({
			"ok": True,
			"result": model_to_dict(auth_models[0]),
		})

	# Keep trying to get an authenticator until a unique one is found
	result = True
	while result:
		authenticator = hmac.new(key=settings.SECRET_KEY.encode('utf-8'), msg=os.urandom(32), digestmod='sha256').hexdigest()
		result = Authenticator.objects.filter(pk=authenticator)

	# Save the authenticator
	auth_model = Authenticator(authenticator=authenticator, user_id=user_id)
	auth_model.save()

	response = {
		"ok": True,
		"result": model_to_dict(auth_model)
	}

	return JsonResponse(response)


def delete(request, authenticator):
	try:
		auth_model = Authenticator.objects.get(pk=authenticator)
	except Authenticator.DoesNotExist:
		return JsonResponse({
				"ok": False,
				"error": "Authenticator does not exist"
			})

	auth_model.delete()

	response = {
		"ok": True,
		"result": {
			"authenticator": authenticator,
		}
	}

	return JsonResponse(response)
