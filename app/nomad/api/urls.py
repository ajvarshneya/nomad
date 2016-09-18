from django.conf.urls import url

from . import views

urlpatterns = [
	# e.g. api/v1/users/1234/
	url(r'^users/(?P<user_id>[0-9]+)/$', views.user.detail, name='users-detail'),

	# e.g. api/v1/users/create
	url(r'^users/create/$', views.user.create, name='users-create')
]



