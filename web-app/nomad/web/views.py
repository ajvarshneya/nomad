from django.http import HttpResponse
from django.template import loader

def index(request):
	template = loader.get_template('web/index.html')
	context = {
		'message': "hacking intensifies!",
	}
	return HttpResponse(template.render(context, request))	
