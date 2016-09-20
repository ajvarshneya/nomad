from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from api.models import Tag, TagForm

def index(request):
	tags = Tag.objects.all()

	tag_dict_list = [model_to_dict(tag) for tag in tags]

	response = {
		"ok": True,
		"result": tag_dict_list
	}
	return JsonResponse(response)

def detail(request, tag_id):
	if request.method == "GET":
		return __detail_get(request, tag_id)
	elif request.method == "POST":
		return __detail_post(request, tag_id)
	elif request.method == "DELETE":
		return __detail_delete(request, tag_id)

def __detail_get(request, tag_id):
	try:
		tag = Tag.objects.get(pk=tag_id)
	except Tag.DoesNotExist:
		return JsonResponse({
				"ok": False,
				"error": "Tag does not exist"
			})

	tag_dict = model_to_dict(tag)

	response = {
		"ok": True,
		"result": tag_dict
	}
	return JsonResponse(response)

def __detail_post(request, tag_id):
	tag_form = TagForm(request.POST)
	if not tag_form.is_valid():
		return JsonResponse({
				"ok": False,
				"error": tag_form.errors
			})

	new_tag = tag_form.save(commit=False)
	new_tag.id = tag_id
	new_tag.save()

	tag_dict = model_to_dict(new_tag)
	response = {
		"ok": True,
		"result": tag_dict
	}
	return JsonResponse(response)

def __detail_delete(request, tag_id):
	try:
		tag = Tag.objects.get(pk=tag_id)
	except Tag.DoesNotExist:
		return JsonResponse({
				"ok": False,
				"error": "Tag does not exist"
			})

	tag.delete()
	response = {
		"ok": True,
		"result": {
			"id": tag_id
		}
	}
	return JsonResponse(response)

def create(request):
	tag_form = TagForm(request.POST)
	if not tag_form.is_valid():
		return JsonResponse({
				"ok": False,
				"error": tag_form.errors
			})

	new_tag = tag_form.save()

	tag_dict = model_to_dict(new_tag)
	response = {
		"ok": True,
		"result": tag_dict
	}
	return JsonResponse(response)