"""
	nomad URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^models/api/v1/', include('models.urls', namespace='models')),
]
