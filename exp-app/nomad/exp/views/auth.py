import urllib.request
import urllib.parse
import json
import requests

from django.http import JsonResponse, QueryDict

def login(request):

    # Check to see if username, password is valid
    data = {}
    data['username'] = request.POST['username']
    data['password'] = request.POST['password']

    url = 'http://models-api:8000/models/api/v1/users/auth/'
    response = requests.post(url, data).json()

    if not response['ok']:
        return JsonResponse({
            'ok': False,
            'error': 'Username or password is incorrect.'
        })

    # Create a new authenticator
    user_id = response['result']['id']
    
    url = 'http://models-api:8000/models/api/v1/auth/create/{}'.format(user_id)
    response = requests.get(url).json()

    if not response['ok']:
        return JsonResponse({
            'ok': False,
            'error': 'Username or password is incorrect.'
        })

    # Return the authenticator
    return JsonResponse(response)

def logout(request):
    
    # Delete the authenticator
    authenticator = request.POST['authenticator']
    url = 'http://models-api:8000/models/api/v1/auth/delete/{}'.format(authenticator)
    
    response = requests.get(url).json()

    if not response['ok']:
        return JsonResponse({
            'ok': False,
            'error': 'Logout failed.'
        })

    return JsonResponse(response)

def create_user(request):

    data = {}
    for field in request.POST:
        data[field] = request.POST[field]

    url = 'http://models-api:8000/models/api/v1/users/create/'

    response = requests.post(url, data).json()

    return JsonResponse(response)

    if not response['ok']:
        return JsonResponse({
            'ok': False,
            'result': None,
            'error': 'Failed to create user.'
        })

    return JsonResponse(response)













