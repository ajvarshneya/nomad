"""
	nomad URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from nomad import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.index),
	url(r'^api/v1/', include('api.urls'))
]
