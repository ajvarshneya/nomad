from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from api.models import *

def index(request):
	reservations = Reservation.objects.all()
	res_dict_list = [model_to_dict(reservation) for reservation in reservations]
	response = {
		"ok":True,
		"result": res_dict_list
	}
	return JsonResponse(response)

def detail(request, reservation_id):
	if request.method == "GET":
		return __detail_get(request, reservation_id)
	elif request.method == "POST":
		return __detail_post(request, reservation_id)
	elif request.method == "DELETE":
		return __detail_delete(request, reservation_id)

def __detail_get(request, reservation_id):
	try:
		reservation = Reservation.objects.get(pk = reservation_id)
	except Reservation.DoesNotExist:
		return JsonResponse({
			"ok": False,
			"error": "Reservation does not exist"
			})
	res_dict = model_to_dict(reservation)
	response = {
		"ok": True,
		"result":res_dict
	}
	return JsonResponse(response)

def __detail_post(request, reservation_id):
	res_form = ReservationForm(request.POST)
	if not res_form.is_valid():
		return JsonResponse({
			"ok": False,
			"error": res_form.errors
			})
	new_res = res_form.save(commit = False)

	new_res.id = reservation_id
	new_res.save()
	res_dict = model_to_dict(new_res)
	response = {
		"ok": True,
		"result" : res_dict
	}
	return JsonResponse(response)

def __detail_delete(request, reservation_id):
	try:
		reservation = Reservation.objects.get(pk=reservation_id)
	except Reservation.DoesNotExist:
		return JsonResponse({
			"ok": False,
			"error": "Reservation does not exist"
			})
	reservation.delete()
	response = {
		"ok": True,
		"result": {
			"id": reservation_id
				}
	}
	return JsonResponse(response)


def create(request):
	res_form = ReservationForm(request.POST)
	#return JsonResponse(request.POST)
	if not res_form.is_valid():
		return JsonResponse({
			"ok": False,
			"error":res_form.errors
			})
	
	new_res = res_form.save()

	res_dict = model_to_dict(new_res)

	response = {
		"ok" : True,
		"result" : res_dict
	}

	return JsonResponse(response)