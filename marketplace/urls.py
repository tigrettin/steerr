from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.make_select_view, name="make-select"),
    url(r'^(?P<make>[-()\w\d\s.,]+)/$', views.model_select_view, name="model-select"),
    url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<model>[-()\w\d\s.,]+)/$', views.platform_select_view, name="platform-select"),
    url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<model>[-()\w\d\s.,]+)/(?P<platform>[-()\w\d\s.,]+)/$', views.body_select_view, name="body-select"),
    url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<model>[-()\w\d\s.,]+)/(?P<platform>[-()\w\d\s.,]+)/(?P<body>[-()\w\d\s.,]+)/$', views.version_select_view, name="version-select"),
    url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<model>[-()\w\d\s.,]+)/(?P<platform>[-()\w\d\s.,]+)/(?P<body>[-()\w\d\s.,]+)/(?P<version>[-()\w\d\s.,]+)/$', views.years_select_view, name="years-select"),
]