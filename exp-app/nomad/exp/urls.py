from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home.index, name='api-index'),
    url(r'^listings/$', views.listings.index, name='listings-index'),
]