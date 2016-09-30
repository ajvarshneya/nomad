from django.db import models
from django.forms import ModelForm

class CommonInfo(models.Model):
    # Created/updated time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
    	abstract = True

class User(CommonInfo):
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

    def __str__(self):
    	return "{} {} ({})".format(self.first_name, self.last_name, self.email)

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = '__all__'

class Listing(CommonInfo):
	# Every Listing has one User, but a User can have many Listings
	user = models.ForeignKey(User)

	# Display info
	title = models.CharField(max_length=50)

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

	# Price
	price = models.IntegerField(default=100)

	def __str__(self):
		return self.title

class ListingForm(ModelForm):
	class Meta:
		model = Listing
		fields = '__all__'

class Reservation(CommonInfo):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	is_available = models.BooleanField()

	# Every Reservation has one User (the person who reserved), but a User can have
	# many Reservations
	user = models.ForeignKey(User, blank=True, null=True)

	# Every Reservation has one Listing, but a Listing can have many Reservations
	listing = models.ForeignKey(Listing)

	def __str__(self):
		return "{} - {} ({})".format(self.start_date.date(), self.end_date.date(), self.listing.title)

class ReservationForm(ModelForm):
	class Meta:
		model = Reservation
		# exclude = ['user','listing']
		fields = '__all__'

class Review(CommonInfo):
	title = models.CharField(max_length=50)
	comment = models.TextField(max_length=1000)

	# Rating from 1-5
	# Note: min/max value is enforced elsewhere in the app
	rating = models.IntegerField(default=3)

	# Every review has one User (author), but a User can have many Reviews
	user = models.ForeignKey(User)

	# Every review has one Listing, but a Listing can have many Reviews
	listing = models.ForeignKey(Listing)

	def __str__(self):
		return self.title

class ReviewForm(ModelForm):
	class Meta:
		model = Review
		fields = '__all__'

class Tag(CommonInfo):
	text = models.CharField(max_length=20)

	# A Tag can have many Listings, and a Listing can have many Tags
	listings = models.ManyToManyField(Listing)

	def __str__(self):
		return self.text

class TagForm(ModelForm):
	class Meta:
		model = Tag
		fields = '__all__'

class Image(CommonInfo):
	# Url for full size image
	url_full = models.URLField()

	class Meta:
		abstract = True

class ProfileImage(Image):
	# Use related_name so the image can be accessed via user.profile_image
	user = models.OneToOneField(User, related_name='profile_image')

	def __str__(self):
		return "{} {}".format(self.user.username, self.id)

class ListingImage(Image):
	# Use related_name so the images can be accessed via listing.images
	listing = models.ForeignKey(Listing, related_name='images')

	def __str__(self):
		return "{} {}".format(self.listing.title, self.id)