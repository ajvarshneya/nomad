from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
	# Home
    url(r'^$', views.home.index, name='index'),

    # Listings
    url(r'^listings/$', views.listings.index, name='listings-index'),
    url(r'^listings/(?P<listing_id>[0-9]+)/$', views.listings.detail, name='listings-detail'),
    url(r'^listings/create/$', views.listings.create, name='listings-create'),

    # Users
    url(r'^users/create/$', views.users.create, name='users-create'),

    # Auth
    url(r'^login/$', views.auth.login, name='auth-login'),
    url(r'^logout/$', views.auth.logout, name='auth-logout'),
]



