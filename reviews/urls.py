from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)_(?P<version>[-()\w\d\s.,/]+)_(?P<year>[-()\w\d\s.,/&]+)/latest/$', views.car_us_view, name="car-us"),
	url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)_(?P<version>[-()\w\d\s.,/]+)_(?P<year>[-()\w\d\s.,/&]+)/(?P<sort>best)/$', views.car_us_view, name="car-us-sort"),
	url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)_(?P<version>[-()\w\d\s.,/]+)/$', views.year_select_us_view, name="year-select-us"),
    url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<trim>[-()\w\d\s.,/]+)/$', views.version_select_us_view, name="version-select-us"),
    url(r'^us/(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)/$', views.trim_select_us_view, name="trim-select-us"),
    url(r'^us/(?P<make>[-()\w\d\s.,/]+)/$', views.model_select_us_view, name="model-select-us"),
    url(r'^us/$', views.make_select_us_view, name="make-select-us"),   

    url(r'^(?P<make>[-()\w\d\s.,/]+)//(?P<years>.*)_(?P<body_type>[-()\w\d\s.,/?]+)/latest/$', views.car_view, name="car"),
 	url(r'^(?P<make>[-()\w\d\s.,/]+)//(?P<years>.*)_(?P<body_type>[-()\w\d\s.,/?]+)/(?P<sort>best)/$', views.car_view, name="car-sort"),
 	url(r'^(?P<car_id>\d+)/subscribe/$', views.car_subscribe, name="car-subscribe"),
 	url(r'^(?P<car_id>\d+)/subscribe/(?P<sort>us)/$', views.car_subscribe, name="car-subscribe-us"),
 	url(r'^(?P<car_id>\d+)/suggest-picture/$', views.suggest_picture, name="suggest-picture"),

    url(r'^(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<platform>[-()\w\d\s.,/?]+)_(?P<body_type>[-()\w\d\s.,/?]+)_(?P<version>[-()\w\d\s.,/&]+)/$', views.years_select_view, name="years-select"),
	url(r'^(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<platform>[-()\w\d\s.,/?]+)_(?P<body_type>[-()\w\d\s.,/?]+)/$', views.version_select_view, name="version-select"),
    url(r'^(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)_(?P<platform>[-()\w\d\s.,/?]+)/$', views.body_select_view, name="body-select"),
    url(r'^(?P<make>[-()\w\d\s.,/]+)_(?P<model>[-()\w\d\s.,/]+)/$', views.platform_select_view, name="platform-select"),
    url(r'^(?P<make>[-()\w\d\s.,/]+)/$', views.model_select_view, name="model-select"),
    url(r'^$', views.make_select_view, name="make-select"),
]