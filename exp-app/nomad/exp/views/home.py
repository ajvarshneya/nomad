from django.http import HttpResponse
from django.template import loader

def index(request):
	template = loader.get_template('exp/index.html')
	context = {
		'message': "Experience layer online.",
	}
	return HttpResponse(template.render(context, request))	
