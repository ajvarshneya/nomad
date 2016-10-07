9/27/16 Brainstorming
- As a user, I want to search listings by locations.
    - Acceptance: 
        - If user searches for a listing in New York, it shows you only locations in New York
        - If user searches for a listing that matches nothing, it shows a "no matches" page.

- As a user, I want to log in to the system.
    - Acceptance:
        - User can successfully authenticate. 
        - Name appears in top right on bar instead of login button.
        - If user gives an invalid password, they cannot log in and are given an error message.

- As a user, I want to save listings that interest me.
    - Acceptance:
        - When the user presses the "save" button, the item is added to the list of saved listings.

- As a user, I want to write reviews on a listing page and a user page.
    - Acceptance:
        - Can write a review and give it a rating, reviews/ratings correctly updated in database.

- As a user, I want to access a page with all listings.
    - Acceptance:
        - View page, has all listings indexed.
        - If no listings, should be a "no listings" page.

- As a user, I want to see reviews of a listing on it's page.
    - Acceptance:
        - When page is loaded, all reviews of listing are given from API.
        - If no reviews, a "no reviews" message is shown.

- As a user, I want to see information/images about a listing on it's page.
    - Acceptance:
        - Can see title, bedrooms, cost, "host", and other information about listing.
        - If you go to a listing with invalid ID, returns a 404 page.

- As a user, I want to see when a listing is available.
    - Acceptance:
        - A list of date ranges is given from the API when a listing page is loaded.
        - If the listing is not available, an empty list is given from the API.
        - If the listing id is not valid then a 404 page is displayed.

- As a user, I want to make a reservation for a listing.
    - Acceptance:
        - If the listing doesn't exist, no reservation is changed, 404 page is given.
        - If the listing page exists and available in the specified time, reservation made.
        - If the listing page exists and not available in the specified time, "listing unavailable at specified time" message displayed.

- As a user, I want to see the most popular listings on the home page.
    - Acceptance:
        - Three listings with the highest ratings are shown. 

- As a user, I want to see the most recent listings on the home page.
    - Acceptance:
        - Three most recent listings are shown.

- As a user, I want to see the average rating for a listing.
    - Acceptance:
        - The average rating is shown if there are reviews.
        - If there are no ratings, "no ratings" is shown (NOT 0/5).
        - If the ID for the user isn't valid, gives a 404 page.
        
- As a user, I want to be able to see a user profile (see a user profile).
    - Acceptance:
        - User profile shown with name, average rating, selected reviews/comments.
        - If user ID does not exist, then a 404 page is shown.

- As a user, I want to see the average rating for a user.
    - Acceptance:
        - Average of all the reviews for all of the user's listings is shown.
        - If the user has no reviews, then "no ratings" is shown (NOT 0/5).
        - If the ID for the user isn't valid, gives a 404 page.

Questions:
- How long should stories be?
- Should stories just be for features we are building in this project?
- Do we unit test the web API layer or the experience API layer





Start USER STORIES AND CORRESPONDING UNIT TEST
WEB LAYER
-As a User I would like to be able to see the home page when I request the site ------>  HomeViewTests
    -Acceptance: 
        -The home page is shown when requested

-As a User I would like to be able view available Listings ------>  ListingViewTests
    -Acceptance
        - If there are no listings to show then display No listings found
        - If there there is an invalid user id display 404 page with invalid listing id
        - If there are listings to be shown the show the listings

EXP LAYER
- As a User I would like to be able to request a list of users in the form of JSON
        - Acceptance
            - A list of users is returned in the form JSON
- As a User I would like to be able to request a list of reservations that I have in the form of JSON
    -Acceptance
        - A list of reservations is returned for a particular user



