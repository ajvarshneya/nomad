# User Stories and Corresponding Unit Tests

## Project 3

#### WEB LAYER

- As a User I would like to be able to see the home page when I request the site -> HomeViewTests
    - Acceptance: 
        - The home page is shown when requested


#### MODEL LAYER

- As a User I would like to be able view available Listings -> ListingViewTests
    - Acceptance
        - If there are no listings to show then display No listings found
        - If there there is an invalid user id display 404 page with invalid listing id
        - If there are listings to be shown the show the listings
- As a User I would like to be able to get a valid listing by id -> listing_tests.py, test_listing_get_valid
    - Acceptance
        - Returns the appropriate JSON of the listing of the id given
- As a User I would like to be able to delete a valid listing by id -> listing_tests.py, test_listing_delete_valid
    - Acceptance
        - Return a JSON with listing id of listing that was deleted  
- As a User I would like to be able to create a valid listing  -> listing_tests.py, test_listing_post_valid
    - Acceptance
        - Return the modified listing with its new values
- As a User I would like to be able to view a list of all listings  -> listing_tests.py, test_listing_index
    - Acceptance
        - Return a JSON with all the listings

## Project 4

- As a User, I would like to login to the system
    - Tests:
        - models - `authenticator_tests.py`
            - `test_auth_check_valid`
            - `test_auth_check_invalid`
            - `test_auth_create_new`
            - `test_auth_create_existing`
        - exp - `tests.py`
            - `test_login_valid`
            - `test_login_invalid`
- As a User, I would like to logout of the system
    - Tests:
        - models - `authenticator_tests.py`
            - `test_auth_delete_valid`
            - `test_auth_delete_invalid`
        - exp - `tests.py`
            - `test_logout_valid`
            - `test_logout_invalid`
- As a User, I would like to make a new account
    - Tests:
        - models - `user_tests.py`
            - `test_user_create_valid`
            - `test_user_create_invalid`
        - exp - `test.py`
            - `test_create_user_valid`
            - `test_create_user_invalid`
- As a User, I would like to create a new listing
    - Tests:
        - models - `listing_tests.py`
            - `test_listing_create_valid`
            - `test_listing_create_invalid`

## Project 5

- As a User, I would like my listings to be searchable.
    - Tests:
        - exp - `search_tests.py`
            - `test_listing_kafka`
- As a User, I would like to search for available listings.
    - Tests:
        - exp - `search_tests.py`
            - `test_search_results`
            - `test_search_empty`
