
USER STORIES AND CORRESPONDING UNIT TESTS


WEB LAYER
-As a User I would like to be able to see the home page when I request the site ------>  HomeViewTests
    -Acceptance: 
        -The home page is shown when requested


MODEL LAYER
-As a User I would like to be able view available Listings ------>  ListingViewTests
    -Acceptance
        - If there are no listings to show then display No listings found
        - If there there is an invalid user id display 404 page with invalid listing id
        - If there are listings to be shown the show the listings

- As a User I would like to be able to get a valid listing by id ------> listing_tests.py, test_listing_get_valid
    -Acceptance
        - Returns the appropriate JSON of the listing of the id given

- As a User I would like to be able to delete a valid listing by id ------> listing_tests.py, test_listing_delete_valid
    -Acceptance
        -Return a JSON with listing id of listing that was deleted  

- As a User I would like to be able to create a valid listing  ------> listing_tests.py, test_listing_post_valid
    -Acceptance
        -Return the modified listing with its new values

- As a User I would like to be able to view a list of all listings  ------> listing_tests.py, test_listing_index
    -Acceptance
        -Return a JSON with all the listings
