from django.conf.urls import url

from . import views

urlpatterns = [
	# e.g. api/v1/users/1234/
	url(r'^users/(?P<user_id>[0-9]+)/$', views.detail, name='users-detail')
]



