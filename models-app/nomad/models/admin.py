from django.contrib import admin

from models.models import *

admin.site.register(User)

admin.site.register(Listing)

admin.site.register(Reservation)

admin.site.register(Review)

admin.site.register(Tag)
