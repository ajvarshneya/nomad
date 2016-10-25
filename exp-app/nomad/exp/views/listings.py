import urllib.request
import urllib.parse
import json
import requests

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
def most_recent(request):
    response = {}

    # Get listings sorted by create date
    listing_request = urllib.request.Request('http://models-api:8000/models/api/v1/listings/?sort=created_desc')
    json_listing_response = urllib.request.urlopen(listing_request).read().decode('utf-8')
    listing_response = json.loads(json_listing_response)

    # Check for errors
    if not listing_response["ok"]:
        response["result"] = None
        response["ok"] = False
        return JsonResponse(response)

    result = listing_response["result"]

    # Get the limit from the url (or return all if no limit)
    limit = request.GET.get('limit', None)
    if limit:
        result = result[:int(limit)]

    # Send the response back
    response["ok"] = True
    response["result"] = result
    return JsonResponse(response)


# Returns a JSON object for the k most popular listings
def most_popular(request):
    response = {}

    # Note: For scalability, it could be worth looking into keeping an average rating
    #   field in the listing class, that way most_popular could be accomplished with
    #   only 1 url request instead of len(listing) requests.
    #
    #   The rating field would have to be updated whenever a new review is added.

    # Get all listings
    listing_request = urllib.request.Request('http://models-api:8000/models/api/v1/listings/')
    json_listing_response = urllib.request.urlopen(listing_request).read().decode('utf-8')
    listing_response = json.loads(json_listing_response)

    if not listing_response["ok"]:
        response["result"] = None
        response["ok"] = False
        return JsonResponse(response)

    # For each listing, get all of its reviews and average their ratings
    # Add the result to a list of tuples containing (rating, listing)
    rating_listing_list = []
    for listing in listing_response["result"]:
        listing_id = listing["id"]

        reviews_request = urllib.request.Request('http://models-api:8000/models/api/v1/reviews/?listing=' + str(listing_id))
        json_reviews_response = urllib.request.urlopen(reviews_request).read().decode('utf-8')
        reviews_response = json.loads(json_reviews_response)

        # If the response was not ok or there were no ratings, assume rating of 0
        if not reviews_response["ok"] or len(reviews_response["result"]) == 0:
            rating_listing_list.append((0, listing))
        else:
            # Calculate the average rating for a listing by averaging all of its review ratings
            rating_sum = 0.0
            for review in reviews_response["result"]:
                rating_sum += review["rating"]
            num_reviews = len(reviews_response["result"])
            avg_rating = rating_sum / num_reviews

            rating_listing_list.append((avg_rating, listing))

    # Sort the list by rating
    rating_listing_list.sort(key=lambda tup: tup[0], reverse=True)

    # Get the limit from the url (or return all if no limit)
    limit = request.GET.get('limit', None)
    if limit:
        rating_listing_list = rating_listing_list[:int(limit)]

    # Add the rating to each listing and add the listing to the result
    result = []
    for tup in rating_listing_list:
        tup[1]["rating"] = tup[0]
        result.append(tup[1])

    response["ok"] = True
    response["result"] = result
    return JsonResponse(response)

def create(request):
    response = {}

    # Check for authentication via the models layer
    auth = request.POST['auth']
    url = 'http://models-api:8000/models/api/v1/auth/check/{}'.format(auth)
    r = requests.get(url)
    json_response = r.json()

    # Return auth error if auth is not valid
    if not json_response["ok"]:
        response["ok"] = False
        response["error_type"] = "auth"
        response["error"] = "Invalid authentication"
        return JsonResponse(response)

    # Make request to create listing model
    data = {}
    for field in request.POST:
        data[field] = request.POST[field]

    # Set the user from the authenticator
    data['user'] = json_response['result']['user']

    url = 'http://models-api:8000/models/api/v1/listings/create/'
    r = requests.post(url, data)
    json_response = r.json()

    # Check that the model was created successfully
    if not json_response["ok"]:
        response["result"] = None
        response["ok"] = False
        return JsonResponse(response)

    # Return model information
    response["ok"] = True
    response["result"] = json_response["result"]
    return JsonResponse(response)




