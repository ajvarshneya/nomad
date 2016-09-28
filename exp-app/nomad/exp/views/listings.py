import urllib.request
import urllib.parse
import json

from django.http import JsonResponse, QueryDict

def index(request):
    
    models_request = urllib.request.Request('http://models-api:8000/models/api/v1/listings')
    json_response = urllib.request.urlopen(models_request).read().decode('utf-8')
    response = json.loads(json_response)

    return JsonResponse(response)