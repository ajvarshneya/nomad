import urllib.request
import urllib.parse
import json

from django.http import JsonResponse, QueryDict

# Returns a JSON object of all the listings in the database
def index(request):
    response = {}

    # Listings model API call
    index_request = urllib.request.Request('http://models-api:8000/models/api/v1/listings/')
    json_index_response = urllib.request.urlopen(index_request).read().decode('utf-8')
    index_response = json.loads(json_index_response)

    if index_response["ok"]:
        response = index_response
        return JsonResponse(response)
    else:
        response["ok"] = False
        response["error"] = "No listings found."
        return JsonResponse(response)

# Returns a JSON object for a given listing, its user, and the reviews associated with that listing
def detail(request, listing_id):

    response = {}
    response["ok"] = True

    # Listings model API call
    listing_request = urllib.request.Request('http://models-api:8000/models/api/v1/listings/' + str(listing_id))
    json_listing_response = urllib.request.urlopen(listing_request).read().decode('utf-8')
    listing_response = json.loads(json_listing_response)
    
    if not listing_response["ok"]:
        response["result"] = None
        response["ok"] = False
        return JsonResponse(response)

    response["result"] = listing_response["result"]
    user_id = listing_response["result"]["user"]

    # User model API call
    user_request = urllib.request.Request('http://models-api:8000/models/api/v1/users/' + str(user_id))
    json_user_response = urllib.request.urlopen(user_request).read().decode('utf-8')
    user_response = json.loads(json_user_response)
    
    if not user_response["ok"]:
        response["result"] = None
        response["ok"] = False
        return JsonResponse(response)

    response["result"]["user"] = user_response["result"]

    # Reviews model API call
    reviews_request = urllib.request.Request('http://models-api:8000/models/api/v1/reviews/?listing=' + str(listing_id))
    json_reviews_response = urllib.request.urlopen(reviews_request).read().decode('utf-8')
    reviews_response = json.loads(json_reviews_response)
    if not reviews_response["ok"]:
        response["reviews"] = []

    response["result"]["reviews"] = reviews_response["result"]
 
    return JsonResponse(response)

# Returns a JSON object for the k most recent listings 
# def most_recent(request, k):
#     response = {}
#     return JsonResponse(response)