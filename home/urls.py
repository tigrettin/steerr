from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.feed, name = "feed"),
    url(r'^register/$', views.UserFormView.as_view(), name = "register"),
    url(r'^login/$', auth_views.login, name = "login"),
    url(r'^logout/$', auth_views.logout, name = "logout"),
    url(r'^search/$', views.search, name = "search"),

   	url(r'^members/(?P<username>[-\w\d.]+)/(?P<category>\w+)/(?P<content_id>\d+)/vote/$', views.content_vote, name="content-vote"),
   	url(r'^members/(?P<username>[-\w\d.]+)/(?P<category>\w+)/(?P<content_id>\d+)/update/$', views.content_update, name="content-update"),
   	url(r'^members/(?P<username>[-\w\d.]+)/(?P<category>\w+)/(?P<content_id>\d+)/confirm/$', views.content_confirm, name="content-confirm"),
   	url(r'^members/(?P<username>[-\w\d.]+)/(?P<category>\w+)/(?P<content_id>\d+)/delete/$', views.content_delete, name="content-delete"),
	  
    url(r'^members/(?P<username>[-\w\d.]+)/subscribe/$', views.member_subscribe, name="member-subscribe"),
    url(r'^members/(?P<username>[-\w\d.]+)/edit/$', views.member_edit, name="member-edit"),
    url(r'^members/(?P<username>[-\w\d.]+)/$', views.member_view, name="member"),
]
