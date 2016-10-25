from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home.index, name='api-index'),
    url(r'^listings/$', views.listings.index, name='listings-index'),
    url(r'^listings/(?P<listing_id>[0-9]+)/$', views.listings.detail, name='listings-detail'),
    url(r'^listings/most_recent/$', views.listings.most_recent, name='listings-most-recent'),
    url(r'^listings/most_popular/$', views.listings.most_popular, name='listings-most-popular'),
    url(r'^listings/create/$', views.listings.create, name='listings-create'),
    url(r'^auth/login$', views.auth.login, name='auth-login'),
    url(r'^auth/logout$', views.auth.logout, name='auth-logout'),
    url(r'^auth/create_user$', views.auth.create_user, name='auth-create-user')
]