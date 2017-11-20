from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)_(?P<version>[-()\w\d\s.,/]+)_(?P<year>[-()\w\d\s.,/&]+)/listings/(?P<listing_id>\d+)/$', views.car_listing_us_view, name="car-listing-us"),
	url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)_(?P<version>[-()\w\d\s.,/]+)_(?P<year>[-()\w\d\s.,/&]+)/listings/$', views.car_listings_us_view, name="car-listings-us"),
	url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)_(?P<version>[-()\w\d\s.,/]+)_(?P<year>[-()\w\d\s.,/&]+)/new-listing/$', views.new_listing_us_view, name="new-listing-us"),
	
	url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)_(?P<version>[-()\w\d\s.,/]+)/$', views.year_select_us_view, name="year-select-us"),
	url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)/$', views.version_select_us_view, name="version-select-us"),
	url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)/$', views.trim_select_us_view, name="trim-select-us"),
    url(r'^us/(?P<make>[-()\w\d\s.,/]+)/$', views.model_select_us_view, name="model-select-us"),
    url(r'^us/$', views.make_select_us_view, name="make-select-us"),

    url(r'^(?P<make>[-()\w\d\s.,/]+)//(?P<years>.*)_(?P<body_type>[-()\w\d\s.,/?]+)/listings/(?P<listing_id>\d+)/$', views.car_listing_view, name="car-listing"),
    url(r'^(?P<make>[-()\w\d\s.,/]+)//(?P<years>.*)_(?P<body_type>[-()\w\d\s.,/?]+)/listings/$', views.car_listings_view, name="car-listings"),
	url(r'^(?P<make>[-()\w\d\s.,/]+)//(?P<years>.*)_(?P<body_type>[-()\w\d\s.,/?]+)/new-listing/$', views.new_listing_view, name="new-listing"),

    url(r'^(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<platform>[-()\w\d\s.,/?]+)_(?P<body_type>[-()\w\d\s.,/?]+)_(?P<version>[-()\w\d\s.,/&]+)/$', views.years_select_view, name="years-select"),
	url(r'^(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<platform>[-()\w\d\s.,/?]+)_(?P<body_type>[-()\w\d\s.,/?]+)/$', views.version_select_view, name="version-select"),
	url(r'^(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<platform>[-()\w\d\s.,/?]+)/$', views.body_select_view, name="body-select"),
	url(r'^(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)/$', views.platform_select_view, name="platform-select"),
    url(r'^(?P<make>[-()\w\d\s.,/]+)/$', views.model_select_view, name="model-select"),
    url(r'^$', views.make_select_view, name="make-select"),
]