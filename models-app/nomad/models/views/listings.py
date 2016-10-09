from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from models.models import *

def index(request):
	listings = Listing.objects.all()

	# Filter by user id
	user_id = int(request.GET.get('user', -1))
	if user_id != -1:
		listings = listings.filter(user_id=user_id)
		# listings = [listing for listing in listings if listing.user.id == user_id]

	# Filter by country
	country = request.GET.get('country', None)
	if country:
		listings = listings.filter(country=country)
		# listings = [listing for listing in listings if listing.country == country]

	# Check for sort order
	sort_param = request.GET.get('sort', None)
	if sort_param == "created_desc":
		listings = listings.order_by('-created_at')
	elif sort_param == "price_desc":
		listings = listings.order_by('-price')
	elif sort_param == "price_asc":
		listings = listings.order_by('price')

	listing_dict_list = [__listing_to_dict(listing) for listing in listings]

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
		return JsonResponse({
				"ok": False,
				"error": "Listing does not exist",
			})

	listing_dict = __listing_to_dict(listing)

	response = {
		"ok": True,
		"result": listing_dict,
	}

	return JsonResponse(response)

def __detail_post(request, listing_id):
	try:
		listing = Listing.objects.get(pk=listing_id)
	except Listing.DoesNotExist:
		return JsonResponse({
				"ok": False,
				"error": "Listing does not exist",
			})

	listing_form = ListingForm(request.POST, instance=listing)

	if not listing_form.is_valid():
		return JsonResponse({
				"ok": False,
				"error": listing_form.errors
			})

	new_listing = listing_form.save(commit=False)

	new_listing.id = int(listing_id)
	new_listing.save()

	listing_dict = __listing_to_dict(new_listing)

	response = {
		"ok": True,
		"result": listing_dict,
	}

	return JsonResponse(response)

def __detail_delete(request, listing_id):
	try:
		listing = Listing.objects.get(pk=listing_id)
	except Listing.DoesNotExist:
		return JsonResponse({
				"ok": False,
				"error": "Listing does not exist"
			})

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
		return JsonResponse({
				"ok": False,
				"error": listing_form.errors
			})

	new_listing = listing_form.save()

	listing_dict = __listing_to_dict(new_listing)

	response = {
		"ok": True,
		"result": listing_dict
	}

	return JsonResponse(response)

def __listing_to_dict(listing):
	listing_dict = model_to_dict(listing)

	listing_dict['created_at'] = listing.created_at
	listing_dict['updated_at'] = listing.updated_at

	# Get all images for the listing and remove redundant listing id info on each image
	image_dict_list = [model_to_dict(image) for image in listing.images.all()]
	for image_dict in image_dict_list:
		image_dict.pop('listing', None)
	listing_dict['images'] = image_dict_list

	return listing_dict
