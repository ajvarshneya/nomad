from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from api.models import *

def index(request):
	listings = Listing.objects.all()

	# Filter by user id
	user_id = int(request.GET.get('user', -1))
	if user_id != -1:
		listings = [listing for listing in listings if listing.user.id == user_id]

	# Filter by country
	country = request.GET.get('country', None)
	if country:
		listings = [listing for listing in listings if listing.country == country]

	listing_dict_list = [model_to_dict(listing) for listing in listings]

	response = {
		"ok": True,
		"result": listing_dict_list
	}

	return JsonResponse(response)

def detail(request, listing_id):
	if request.method == "GET":
		return __detail_get(request, listing_id)
	elif request.method == "POST":
		return __detail_post(request, listing_id)
	elif request.method == "DELETE":
		return __detail_delete(request, listing_id)

def __detail_get(request, listing_id):
	try:
		listing = Listing.objects.get(pk=listing_id)
	except Listing.DoesNotExist:
		return JsonResponse({"ok": False})

	listing_dict = model_to_dict(listing)

	response = {
		"ok": True,
		"result": listing_dict,
	}

	return JsonResponse(response)

def __detail_post(request, listing_id):
	listing_form = ListingForm(request.POST)

	if not listing_form.is_valid():
		return JsonResponse({"ok": False})

	new_listing = listing_form.save(commit=False)

	new_listing.id = listing_id
	new_listing.save()

	listing_dict = model_to_dict(new_listing)

	response = {
		"ok": True,
		"result": listing_dict,
	}

	return JsonResponse(response)

def __detail_delete(request, listing_id):
	try:
		listing = Listing.objects.get(pk=listing_id)
	except Listing.DoesNotExist:
		return JsonResponse({"ok": False})

	listing.delete()

	response = {
		"ok": True,
		"result": {
			"id": listing_id
		}
	}

	return JsonResponse(response)

def create(request):
	listing_form = ListingForm(request.POST)

	# return JsonResponse(request.POST)

	if not listing_form.is_valid():
		return JsonResponse({"ok": False})

	new_listing = listing_form.save()

	listing_dict = model_to_dict(new_listing)

	response = {
		"ok": True,
		"result": listing_dict
	}

	return JsonResponse(response)
