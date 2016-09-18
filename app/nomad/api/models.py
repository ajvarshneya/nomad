from django.db import models
from django.forms import ModelForm

class User(models.Model):
	# Contact info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)

    # Login info
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=50)

    # Payment info
    creditcard = models.CharField(max_length=17)

    # Address info
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=9)

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'email',
			'phone_number',
			'password',
			'username',
			'creditcard',
			'street',
			'city',
			'country',
			'zipcode'
		]

class Listing(models.Model):
	# Every Listing has one User, but a User can have many Listings
	user = models.ForeignKey(User)

	# Address info
	street = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	zipcode = models.CharField(max_length=9)

	# Number of beds available
	beds = models.IntegerField(default=1)

	# Number of baths as a decimal number with format ###.#
	# This allows users to specify 2.5 baths, etc.
	baths = models.DecimalField(max_digits=4, decimal_places=1)

class ListingForm(ModelForm):
	class Meta:
		model = Listing
		fields = [
			'user',
			'street',
			'city',
			'country',
			'zipcode',
			'beds',
			'baths'
		]

class Reservation(models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	is_available = models.BooleanField()

	# Every Reservation has one User (the person who reserved), but a User can have
	# many Reservations
	user = models.ForeignKey(User)

	# Every Reservation has one Listing, but a Listing can have many Reservations
	listing = models.ForeignKey(Listing)

class ReservationForm(ModelForm):
	class Meta:
		model = Reservation
		fields = [
			'start_date',
			'end_date',
			'is_available',
			'user',
			'listing'
		]

class Review(models.Model):
	title = models.CharField(max_length=50)
	comment = models.TextField(max_length=1000)

	# Rating from 1-5
	# Note: min/max value is enforced elsewhere in the app
	rating = models.IntegerField(default=3)

	# Every review has one User (author), but a User can have many Reviews
	user = models.ForeignKey(User)

	# Every review has one Listing, but a Listing can have many Reviews
	listing = models.ForeignKey(Listing)

class ReviewModel(ModelForm):
	class Meta:
		model = Review
		fields = [
			'title',
			'comment',
			'rating',
			'user',
			'listing'
		]

class Tag(models.Model):
	text = models.CharField(max_length=20)

	# A Tag can have many Listings, and a Listing can have many Tags
	listings = models.ManyToManyField(Listing)

class TagForm(ModelForm):
	class Meta:
		model = Tag
		fields = [
			'text',
			'listing'
		]