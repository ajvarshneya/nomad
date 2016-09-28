from django.http import HttpResponse
from django.template import loader

def index(request):
	template = loader.get_template('web/listings.html')
	context = {
		'listings': ["a", "b", "c", "d"],
	}	
	return HttpResponse(template.render(context, request))


	
