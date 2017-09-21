from django.conf.urls import url, include
from django.contrib import admin
import reviews, marketplace


urlpatterns = [

	url(r'^admin/', admin.site.urls),
	url(r'^', include("home.urls", namespace="home")),
	url(r'^reviews/', include("reviews.urls", namespace="reviews")),
	url(r'^marketplace/', include("marketplace.urls", namespace="marketplace")),
	url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<years>.*)/listings/(?P<listing_id>\d+)/$', marketplace.views.car_listing_view, name="car-listing"),
	url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<years>.*)/listings/$', marketplace.views.car_listings_view, name="car-listings"),
	url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<years>.*)/new-listing/$', marketplace.views.new_listing_view, name="new-listing"),
	url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<years>.*)/subscribe/$', reviews.views.car_subscribe, name="car-subscribe"),
	url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<years>.*)/(?P<review_id>\d+)/vote/$', reviews.views.review_vote, name="review-vote"), 
	url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<years>.*)/(?P<sort>\w+)/$', reviews.views.car_view, name="car-sort"),
	url(r'^(?P<make>[-()\w\d\s.,]+)/(?P<years>.*)/$', reviews.views.car_view, name="car"),
]