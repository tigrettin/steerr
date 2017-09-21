from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.feed, name = "feed"),
    url(r'^register/$', views.UserFormView.as_view(), name = "register"),
    url(r'^login/$', auth_views.login, name = "login"),
    url(r'^logout/$', auth_views.logout, name = "logout"),
   	url(r'^members/(?P<username>[-\w\d.]+)/(?P<opinion_id>\d+)/vote/$', views.opinion_vote, name="opinion-vote"),
	url(r'^members/(?P<username>[-\w\d.]+)/subscribe/$', views.member_subscribe, name="member-subscribe"),
   	url(r'^members/(?P<username>[-\w\d.]+)/$', views.member_view, name="member"),
]
