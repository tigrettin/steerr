from django import forms
from django.db.models import Avg, Min, Max
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from home.models import Subscriptions
from marketplace.models import Listing
from num2words import num2words
from pathlib import Path
from .forms import MakeSelectForm, ModelSelectForm, PlatformSelectForm, BodySelectForm, VersionSelectForm, YearsSelectForm, ReviewForm
from .models import Car, Review


def make_select_view(request):
	if request.GET.get("submitted", None):
		form = MakeSelectForm(request.GET)
		if form.is_valid():
			make = form.cleaned_data['make']
			return redirect("reviews:model-select", make=make)
	else:
		form = MakeSelectForm()
	reviews = Review.objects.all().order_by('-created')
	context = {"form": form, "reviews": reviews}
	return render(request, "reviews/carselect.html", context)


def model_select_view(request, make):
	model = None
	if request.GET.get("submitted", None):
		form = ModelSelectForm(request.GET, make=make)
		if form.is_valid():
			model = form.cleaned_data['model']
			return redirect("reviews:platform-select", make=make, model=model)
	else:
		form = ModelSelectForm(make=make)
	reviews = Review.objects.filter(car__make=make).order_by('-created')
	context = {"form": form, "make": make, "reviews": reviews}
	return render(request, "reviews/carselect.html", context)


def platform_select_view(request, make, model):
	platform = None
	if request.GET.get("submitted", None):
		form = PlatformSelectForm(request.GET, make=make, model=model)
		if form.is_valid():
			platform = form.cleaned_data['platform']
			return redirect("reviews:body-select", make=make, model=model, platform=platform)       
	else:
		form = PlatformSelectForm(make=make, model=model)
	reviews = Review.objects.filter(car__make=make, car__model=model).order_by('-created')
	context = {"form": form, "make": make, "model": model, "reviews": reviews}
	return render(request, "reviews/carselect.html", context)


def body_select_view(request, make, model, platform):
	body = None
	if request.GET.get("submitted", None):
		form = BodySelectForm(request.GET, make=make, model=model, platform=platform)
		if form.is_valid():
			body = form.cleaned_data['body']
			return redirect("reviews:version-select", make=make, model=model, platform=platform, body=body)
	else:
		form = BodySelectForm(make=make, model=model, platform=platform)
	reviews = Review.objects.filter(car__make=make, car__model=model, car__platform=platform).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "reviews": reviews}
	return render(request, "reviews/carselect.html", context)


def version_select_view(request, make, model, platform, body):
	version = None
	if request.GET.get("submitted", None):
		form = VersionSelectForm(request.GET, make=make, model=model, platform=platform, body=body)
		if form.is_valid():
			version = form.cleaned_data['version']
			return redirect("reviews:years-select", make=make, model=model, platform=platform, body=body, version=version)       
	else:
		form = VersionSelectForm(make=make, model=model, platform=platform, body=body)
	reviews = Review.objects.filter(car__make=make, car__model=model, car__platform=platform, car__body=body).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "body": body, "reviews": reviews}
	return render(request, "reviews/carselect.html", context)


def years_select_view(request, make, model, platform, body, version):
	years = None
	if request.GET.get("submitted", None):
		form = YearsSelectForm(request.GET, make=make, model=model, platform=platform, body=body, version=version)
		if form.is_valid():
			years = form.cleaned_data['years']
			return redirect("car", make=make, years=years)
	else:
		form = YearsSelectForm(make=make, model=model, platform=platform, body=body, version=version)
	reviews = Review.objects.filter(car__make=make, car__model=model, car__platform=platform, car__body=body, car__version=version).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "body": body, "version": version, "reviews": reviews}
	return render(request, "reviews/carselect.html", context)


def car_view(request, make, years, sort=None):
	if len(Car.objects.filter(make=make, years=years)) == 1:
		multiple = False
		car = Car.objects.get(make=make, years=years)
	else:
		multiple = True
		car = Car.objects.get(make=make, years=years, no_of_doors=3)

	doors = num2words(int(car.no_of_doors))
	seats = num2words(int(car.no_of_seats))
	car_image = Path("C:/Users/And/Desktop/steerr/static/reviews/images/" + str(car) + ".jpg")
	review_users = Review.objects.filter(car=car).values_list('user',flat=True)

	if Listing.objects.filter(car=car):
		min_price = Listing.objects.filter(car=car).order_by('price')[0].price
		max_price = Listing.objects.filter(car=car).order_by('-price')[0].price
	else:
		min_price = None
		max_price = None

	if Review.objects.filter(car=car):
		total = 0
		total_rating = 0
		for review in Review.objects.filter(car=car):
			total_rating += review.rating * (1.5**review.vote_score)
			total += (1.5**review.vote_score)
		average_rating = round(total_rating/total,1)
		#average_rating = round(Review.objects.filter(car=car).aggregate(Avg('rating'))['rating__avg'],1)
	else:
		average_rating = None

	form = ReviewForm(initial={'rating': ''})
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			review = form.save(commit=False)
			review.text = form.cleaned_data['text']
			review.title = form.cleaned_data['title']
			review.rating = form.cleaned_data['rating']
			review.car = car
			review.user = request.user
			review.save()
			return redirect("car", make=make, years=years)

	if sort == None:
		reviews = Review.objects.filter(car=car).reverse()
	elif sort == 'best':
		reviews = Review.objects.filter(car=car).order_by('-vote_score')

	context = {"car": car, 
	"car_image": car_image, 
	"multiple": multiple, 
	"doors": doors, 
	"seats": seats, 
	"average_rating": average_rating, 
	"form": form, 
	"review_users": review_users,
	"min_price": min_price,
	"max_price": max_price,
	"reviews": reviews,
	"sort": sort}

	return render(request, "reviews/car.html", context)


def review_vote(request, make, years, review_id):
	review = Review.objects.get(id=review_id)

	if review.user != request.user:
		if "vote-up" in request.GET:
			review.votes.up(request.user.id)
		elif "vote-down" in request.GET:
			review.votes.down(request.user.id)

	return redirect("car", make=make, years=years)


def car_subscribe(request, make, years):
	if len(Car.objects.filter(make=make, years=years)) == 1:
		car = Car.objects.get(make=make, years=years)
	else:
		car = Car.objects.get(make=make, years=years, no_of_doors=3)

	subs, created = Subscriptions.objects.get_or_create(user=request.user)
	if "subscribe" in request.GET:
		subs.cars.add(car)
	elif "unsubscribe" in request.GET:
		subs.cars.remove(car)

	return redirect("car", make=make, years=years)