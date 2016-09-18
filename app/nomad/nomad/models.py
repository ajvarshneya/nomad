from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    creditcard = models.CharField(max_length=17)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=9)

class Listing(models.Model):
	# Every Listing has one User, but a User can have many Listings
	user = models.ForeignKey(User)

	# Address info
	street = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	zipcode = models.CharField(max_length=9)

	# Number of beds available
	beds = IntegerField(default=1)

	# Number of baths as a decimal number with format ###.#
	# This allows users to specify 2.5 baths, etc.
	baths = DecimalField(max_digits=4, decimal_places=1)

class Reservation(models.Model):
	pass

class Review(models.Model):
	title = models.CharField(50)
	comment = models.TextField(max_length=1000)

	# Rating from 1-5
	# Note: min/max value is enforced elsewhere in the app
	rating = models.IntegerField(default=3)

	# Every review has one User (author), but a User can have many Reviews
	user = models.ForeignKey(User)

	# Every review has one Listing, but a Listing can have many Reviews
	listing = models.ForeignKey(Listing)

class Tag(models.Model):
	text = models.CharField(20)

	# A Tag can have many Listings, and a Listing can have many Tags
	listings = models.ManyToManyField(Listing)
