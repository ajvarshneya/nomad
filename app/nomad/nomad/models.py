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
	pass

class Reservation(models.Model):
	pass

class Review(models.Model):
	pass

class Tag(models.Model):
	pass
