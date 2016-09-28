from django.http import HttpResponse
from django.template import loader

def index(request):
	template = loader.get_template('models/index.html')
	context = {
		'message': "Models layer online.",
	}
	return HttpResponse(template.render(context, request))	
