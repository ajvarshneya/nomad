from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from models.models import *

def index(request):
	reservations = Reservation.objects.all()

	# Filter by user id
	user_id = int(request.GET.get('user', -1))
	if user_id != -1:
		reservations = [res for res in reservations if res.user.id == user_id]

	# Filter by listing id
	listing_id = int(request.GET.get('listing', -1))
	if listing_id != -1:
		reservations = [res for res in reservations if res.listing.id == listing_id]

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
