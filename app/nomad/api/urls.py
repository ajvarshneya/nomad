from django.conf.urls import url

from . import views

urlpatterns = [
	# e.g. api/v1/users/
	url(r'^users/$', views.users.index, name='users-index'),

	# e.g. api/v1/users/1234/
	url(r'^users/(?P<user_id>[0-9]+)/$', views.users.detail, name='users-detail'),

	# e.g. api/v1/users/create/
	url(r'^users/create/$', views.users.create, name='users-create'),

	# e.g. api/v1/listings/
	url(r'^listings/$', views.listings.index, name='listings-index'),

	# e.g. api/v1/listings/1234/
	url(r'^listings/(?P<listing_id>[0-9]+)/$', views.listings.detail, name='listings-detail'),

	# e.g. api/v1/listings/create/
	url(r'^listings/create/$', views.listings.create, name='listings-create'),

	# e.g. api/v1/reservations/
	url(r'^reservations/$', views.reservations.index, name="reservations-index"),

	# e.g. api/v1/reservations/1234
	url(r'^reservations/(?P<reservation_id>[0-9]+)/$', views.reservations.detail, name='reservations-detail'),

	# e.g. api/v1/reservations/create
	url(r'^reservations/create/$', views.reservations.create, name='reservations-create'),

	# e.g. api/v1/reviews/
	url(r'^reviews/$', views.reviews.index, name='reviews-index'),

	# e.g. api/v1/reviews/1234
	url(r'^reviews/(?P<review_id>[0-9]+)/$', views.reviews.detail, name='reviews-detail'),

	# e.g. api/v1/reviews/create
	url(r'^reviews/create/$', views.reviews.create, name='reviews-create'),

	# e.g. api/v1/tags/
	url(r'^tags/$', views.tags.index, name='tags-index'),

	# e.g. api/v1/tags/1234
	url(r'^tags/(?P<tag_id>[0-9]+)/$', views.tags.detail, name='tags-detail'),

	# e.g. api/v1/tags/create
	url(r'^tags/create/$', views.tags.create, name='tags-detail'),

]



