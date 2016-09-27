from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from api.models import Review, ReviewForm

def index(request):
	reviews = Review.objects.all()

	# Filter by user id
	user_id = int(request.GET.get('user', -1))
	if user_id != -1:
		reviews = [review for review in reviews if review.user.id == user_id]

	# Filter by listing id
	listing_id = int(request.GET.get('listing', -1))
	if listing_id != -1:
		reviews = [review for review in reviews if review.listing.id == listing_id]

	review_dict_list = [model_to_dict(review) for review in reviews]

	response = {
		"ok": True,
		"result": review_dict_list,
	}

	return JsonResponse(response)

def detail(request, review_id):
	if request.method == "GET":
		return __detail_get(request, review_id)
	elif request.method == "POST":
		return __detail_post(request, review_id)
	elif request.method == "DELETE":
		return __detail_delete(request, review_id)

def __detail_get(request, review_id):
	try:
		review = Review.objects.get(pk=review_id)
	except Review.DoesNotExist:
		return JsonResponse({
				"ok": False,
				"error": "Review does not exist"
			})

	review_dict = model_to_dict(review)

	response = {
		"ok": True,
		"result": review_dict,
	}

	return JsonResponse(response)

def __detail_post(request, review_id):
	review_form = ReviewForm(request.POST)
	if not review_form.is_valid():
		return JsonResponse({
				"ok": False,
				"error": review_form.errors
			})

	new_review = review_form.save(commit=False)
	new_review.id = review_id
	new_review.save()

	review_dict = model_to_dict(new_review)
	response = {
		"ok": True,
		"result": review_dict
	}
	return JsonResponse(response)

def __detail_delete(request, review_id):
	try:
		review = Review.objects.get(pk=review_id)
	except Review.DoesNotExist:
		return JsonResponse({
				"ok": False,
				"error": "Review does not exist",
			})

	review.delete()
	response = {
		"ok": True,
		"result": {
			"id": review_id
		}
	}
	return JsonResponse(response)

def create(request):
	review_form = ReviewForm(request.POST)
	if not review_form.is_valid():
		return JsonResponse({
				"ok": False,
				"error": review_form.errors
			})

	new_review = review_form.save()

	review_dict = model_to_dict(new_review)
	response = {
		"ok": True,
		"result": review_dict,
	}
	return JsonResponse(response)
