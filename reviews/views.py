from django import forms
from django.contrib import messages
from django.db.models import Avg, Min, Max
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from home.models import Subscriptions
from marketplace.models import Listing, ListingUS
from pathlib import Path
from .models import Car, CarUS, Review, ReviewUS, SuggestedPicture
from . import forms


def make_select_view(request):
	if request.GET.get("submitted", None):
		form = forms.MakeSelectForm(request.GET)
		if form.is_valid():
			make = form.cleaned_data['make']
			models = Car.objects.filter(make=make).values_list('model',flat=True).distinct()
			if len(models) == 1:
				model = models[0]
				platforms = Car.objects.filter(make=make, model=model).values_list('platform',flat=True).distinct()
				if len(platforms) == 1:
					platform = platforms[0]
					body_types = Car.objects.filter(make=make, model=model, platform=platform).values_list('body_type',flat=True).distinct()
					if len(body_types) == 1:
						body_type = body_types[0]
						versions = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type).values_list('version',flat=True).distinct()
						if len(versions) == 1:
							version = versions[0]
							yearss = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type, version=version).values_list('years',flat=True).distinct()
							if len(yearss) == 1:
								years = yearss[0]
								return redirect("reviews:car", make=make, years=years, body_type=body_type)
							else:
								return redirect("reviews:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)
						else:
							return redirect("reviews:version-select", make=make, model=model, platform=platform, body_type=body_type)
					else:
						return redirect("reviews:body-select", make=make, model=model, platform=platform)
				else:
					return redirect("reviews:platform-select", make=make, model=model)
			else:
				return redirect("reviews:model-select", make=make)
	else:
		form = forms.MakeSelectForm()
	reviews = Review.objects.all().order_by('-created')
	context = {"form": form, "reviews": reviews}
	return render(request, "reviews/car-select.html", context)


def model_select_view(request, make):
	model = None
	if request.GET.get("submitted", None):
		form = forms.ModelSelectForm(request.GET, make=make)
		if form.is_valid():
			model = form.cleaned_data['model']
			platforms = Car.objects.filter(make=make, model=model).values_list('platform',flat=True).distinct()
			if len(platforms) == 1:
				platform = platforms[0]
				body_types = Car.objects.filter(make=make, model=model, platform=platform).values_list('body_type',flat=True).distinct()
				if len(body_types) == 1:
					body_type = body_types[0]
					versions = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type).values_list('version',flat=True).distinct()
					if len(versions) == 1:
						version = versions[0]
						yearss = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type, version=version).values_list('years',flat=True).distinct()
						if len(yearss) == 1:
							years = yearss[0]
							return redirect("reviews:car", make=make, years=years, body_type=body_type)
						else:
							return redirect("reviews:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)
					else:
						return redirect("reviews:version-select", make=make, model=model, platform=platform, body_type=body_type)
				else:
					return redirect("reviews:body-select", make=make, model=model, platform=platform)
			else:
				return redirect("reviews:platform-select", make=make, model=model)
	else:
		form = forms.ModelSelectForm(make=make)
	reviews = Review.objects.filter(car__make=make).order_by('-created')
	context = {"form": form, "make": make, "reviews": reviews}
	return render(request, "reviews/car-select.html", context)


def platform_select_view(request, make, model):
	platform = None
	if request.GET.get("submitted", None):
		form = forms.PlatformSelectForm(request.GET, make=make, model=model)
		if form.is_valid():
			platform = form.cleaned_data['platform']
			body_types = Car.objects.filter(make=make, model=model, platform=platform).values_list('body_type',flat=True).distinct()
			if len(body_types) == 1:
				body_type = body_types[0]
				versions = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type).values_list('version',flat=True).distinct()
				if len(versions) == 1:
					version = versions[0]
					yearss = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type, version=version).values_list('years',flat=True).distinct()
					if len(yearss) == 1:
						years = yearss[0]
						return redirect("reviews:car", make=make, years=years, body_type=body_type)
					else:
						return redirect("reviews:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)
				else:
					return redirect("reviews:version-select", make=make, model=model, platform=platform, body_type=body_type)
			else:
				return redirect("reviews:body-select", make=make, model=model, platform=platform)       
	else:
		form = forms.PlatformSelectForm(make=make, model=model)
	reviews = Review.objects.filter(car__make=make, car__model=model).order_by('-created')
	context = {"form": form, "make": make, "model": model, "reviews": reviews}
	return render(request, "reviews/car-select.html", context)


def body_select_view(request, make, model, platform):
	body_type = None
	if request.GET.get("submitted", None):
		form = forms.BodySelectForm(request.GET, make=make, model=model, platform=platform)
		if form.is_valid():
			body_type = form.cleaned_data['body']
			versions = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type).values_list('version',flat=True).distinct()
			if len(versions) == 1:
				version = versions[0]
				yearss = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type, version=version).values_list('years',flat=True).distinct()
				if len(yearss) == 1:
					years = yearss[0]
					return redirect("reviews:car", make=make, years=years, body_type=body_type)
				else:
					return redirect("reviews:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)
			else:
				return redirect("reviews:version-select", make=make, model=model, platform=platform, body_type=body_type)
	else:
		form = forms.BodySelectForm(make=make, model=model, platform=platform)
	reviews = Review.objects.filter(car__make=make, car__model=model, car__platform=platform).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "reviews": reviews}
	return render(request, "reviews/car-select.html", context)


def version_select_view(request, make, model, platform, body_type):
	version = None
	if request.GET.get("submitted", None):
		form = forms.VersionSelectForm(request.GET, make=make, model=model, platform=platform, body_type=body_type)
		if form.is_valid():
			version = form.cleaned_data['version']
			yearss = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type, version=version).values_list('years',flat=True).distinct()
			if len(yearss) == 1:
				years = yearss[0]
				return redirect("reviews:car", make=make, years=years, body_type=body_type)
			else:
				return redirect("reviews:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)       
	else:
		form = forms.VersionSelectForm(make=make, model=model, platform=platform, body_type=body_type)
	reviews = Review.objects.filter(car__make=make, car__model=model, car__platform=platform, car__body_type=body_type).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "body_type": body_type, "reviews": reviews}
	return render(request, "reviews/car-select.html", context)


def years_select_view(request, make, model, platform, body_type, version):
	years = None
	if request.GET.get("submitted", None):
		form = forms.YearsSelectForm(request.GET, make=make, model=model, platform=platform, body_type=body_type, version=version)
		if form.is_valid():
			years = form.cleaned_data['years']
			return redirect("reviews:car", make=make, years=years, body_type=body_type)
	else:
		form = forms.YearsSelectForm(make=make, model=model, platform=platform, body_type=body_type, version=version)
	reviews = Review.objects.filter(car__make=make, car__model=model, car__platform=platform, car__body_type=body_type, car__version=version).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "body_type": body_type, "version": version, "reviews": reviews}
	return render(request, "reviews/car-select.html", context)


def car_view(request, make, years, body_type, sort=None):
	if len(Car.objects.filter(make=make, years=years, body_type=body_type)) == 1:
		car = Car.objects.get(make=make, years=years, body_type=body_type)
		doors = car.no_of_doors
	else:
		doors_min = Car.objects.filter(make=make, years=years, body_type=body_type).aggregate(Min('no_of_doors'))['no_of_doors__min']
		doors_max = Car.objects.filter(make=make, years=years, body_type=body_type).aggregate(Max('no_of_doors'))['no_of_doors__max']
		doors = doors_min+"/"+doors_max
		car = Car.objects.get(make=make, years=years, body_type=body_type, no_of_doors=doors_min)

	try:
		already_suggested = SuggestedPicture.objects.filter(car=car, user=request.user)
	except:
		already_suggested = False

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

	form = forms.ReviewForm(initial={'rating': ''})
	if request.method == 'POST':
		form = forms.ReviewForm(request.POST)
		if form.is_valid():
			review = form.save(commit=False)
			review.text = form.cleaned_data['text']
			review.title = form.cleaned_data['title']
			review.rating = form.cleaned_data['rating']
			review.car = car
			review.user = request.user
			review.save()
			messages.success(request, 'Your review has been published!')
			return redirect("reviews:car", make=make, years=years, body_type=body_type)

	if sort == None:
		reviews = Review.objects.filter(car=car).reverse()
	elif sort == 'best':
		reviews = Review.objects.filter(car=car).order_by('-vote_score')

	context = {"car": car,
	"already_suggested": already_suggested,
	"doors": doors,
	"average_rating": average_rating, 
	"form": form, 
	"review_users": review_users,
	"min_price": min_price,
	"max_price": max_price,
	"reviews": reviews,
	"sort": sort}

	return render(request, "reviews/car.html", context)


def car_subscribe(request, car_id, sort=None):
	if sort == None:
		car = Car.objects.get(id=car_id)
		subs, created = Subscriptions.objects.get_or_create(user=request.user)
		if "subscribe" in request.GET:
			subs.cars.add(car)
		elif "unsubscribe" in request.GET:
			subs.cars.remove(car)
		return redirect("reviews:car", make=car.make, years=car.years, body_type=car.body_type)
	elif sort == 'us':
		car = CarUS.objects.get(id=car_id)
		subs, created = Subscriptions.objects.get_or_create(user=request.user)
		if "subscribe" in request.GET:
			subs.cars_us.add(car)
		elif "unsubscribe" in request.GET:
			subs.cars_us.remove(car)
		return redirect("reviews:car-us", make=car.make, model=car.model, trim=car.trim, version=car.version, year=car.year)	


def suggest_picture(request, car_id):
	car = Car.objects.get(id=car_id)
	already_suggested = None

	try:
		suggested = SuggestedPicture.objects.get(car=car, user=request.user)
		already_suggested = suggested.picture
		form = forms.SuggestedPictureForm(request.POST or None, request.FILES or None, instance=suggested)
		if form.is_valid():
			form.save()
			messages.success(request, 'Suggestion updated.')
			return redirect("reviews:car", make=car.make, years=car.years, body_type=car.body_type)
	except:
		form = forms.SuggestedPictureForm()
		if request.method == 'POST':
			form = forms.SuggestedPictureForm(request.POST, request.FILES)
			if form.is_valid():
				suggested = form.save(commit=False)
				suggested.user = request.user
				suggested.car = car
				suggested.picture = form.cleaned_data['picture']
				suggested.save()
				messages.success(request, 'Thank you for your suggestion! We will review your picture as soon as possible.')
				return redirect("reviews:car", make=car.make, years=car.years, body_type=car.body_type)
	context = {
		"car": car,
		"form": form,
		"already_suggested": already_suggested,
	}

	return render(request, "reviews/suggest-picture.html", context)


	### AMERICAN DATABASE ###


def make_select_us_view(request):
	if request.GET.get("submitted", None):
		form = forms.MakeSelectUSForm(request.GET)
		if form.is_valid():
			make = form.cleaned_data['make']
			models = CarUS.objects.filter(make=make).values_list('model',flat=True).distinct()
			if len(models) == 1:
				model = models[0]
				trims = CarUS.objects.filter(make=make, model=model).values_list('trim',flat=True).distinct()
				if len(trims) == 1:
					trim = trims[0]
					versions = CarUS.objects.filter(make=make, model=model, trim=trim).values_list('version',flat=True).distinct()
					if len(versions) == 1:
						version = versions[0]
						years = CarUS.objects.filter(make=make, model=model, trim=trim, version=version).values_list('year',flat=True).distinct()
						if len(years) == 1:
							year = years[0]
							return redirect("reviews:car-us", make=make, model=model, trim=trim, version=version, year=year)
						else:
							return redirect("reviews:year-select-us", make=make, model=model, trim=trim, version=version)
					else:
						return redirect("reviews:version-select-us", make=make, model=model, trim=trim)
				else:
					return redirect("reviews:trim-select-us", make=make, model=model)
			else:
				return redirect("reviews:model-select-us", make=make)
	else:
		form = forms.MakeSelectUSForm()
	reviews = ReviewUS.objects.all().order_by('-created')
	context = {"form": form, "reviews": reviews}
	return render(request, "reviews/us/car-select.html", context)


def model_select_us_view(request, make):
	model = None
	if request.GET.get("submitted", None):
		form = forms.ModelSelectUSForm(request.GET, make=make)
		if form.is_valid():
			model = form.cleaned_data['model']
			trims = CarUS.objects.filter(make=make, model=model).values_list('trim',flat=True).distinct()
			if len(trims) == 1:
				trim = trims[0]
				versions = CarUS.objects.filter(make=make, model=model, trim=trim).values_list('version',flat=True).distinct()
				if len(versions) == 1:
					version = versions[0]
					years = CarUS.objects.filter(make=make, model=model, trim=trim, version=version).values_list('year',flat=True).distinct()
					if len(years) == 1:
						year = years[0]
						return redirect("reviews:car-us", make=make, model=model, trim=trim, version=version, year=year)
					else:
						return redirect("reviews:year-select-us", make=make, model=model, trim=trim, version=version)
				else:
					return redirect("reviews:version-select-us", make=make, model=model, trim=trim)
			else:
				return redirect("reviews:trim-select-us", make=make, model=model)
	else:
		form = forms.ModelSelectUSForm(make=make)
	reviews = ReviewUS.objects.filter(car__make=make).order_by('-created')
	context = {"form": form, "make": make, "reviews": reviews}
	return render(request, "reviews/us/car-select.html", context)


def trim_select_us_view(request, make, model):
	trim = None
	if request.GET.get("submitted", None):
		form = forms.TrimSelectUSForm(request.GET, make=make, model=model)
		if form.is_valid():
			trim = form.cleaned_data['trim']
			versions = CarUS.objects.filter(make=make, model=model, trim=trim).values_list('version',flat=True).distinct()
			if len(versions) == 1:
				version = versions[0]
				years = CarUS.objects.filter(make=make, model=model, trim=trim, version=version).values_list('year',flat=True).distinct()
				if len(years) == 1:
					year = years[0]
					return redirect("reviews:car-us", make=make, model=model, trim=trim, version=version, year=year)
				else:
					return redirect("reviews:year-select-us", make=make, model=model, trim=trim, version=version)
			else:
				return redirect("reviews:version-select-us", make=make, model=model, trim=trim)
	else:
		form = forms.TrimSelectUSForm(make=make, model=model)
	reviews = ReviewUS.objects.filter(car__make=make, car__model=model).order_by('-created')
	context = {"form": form, "make": make, "model": model, "reviews": reviews}
	return render(request, "reviews/us/car-select.html", context)


def version_select_us_view(request, make, model, trim):
	version = None
	if request.GET.get("submitted", None):
		form = forms.VersionSelectUSForm(request.GET, make=make, model=model, trim=trim)
		if form.is_valid():
			version = form.cleaned_data['version']
			years = CarUS.objects.filter(make=make, model=model, trim=trim, version=version).values_list('year',flat=True).distinct()
			if len(years) == 1:
				year = years[0]
				return redirect("reviews:car-us", make=make, model=model, trim=trim, version=version, year=year)
			else:
				return redirect("reviews:year-select-us", make=make, model=model, trim=trim, version=version)
	else:
		form = forms.VersionSelectUSForm(make=make, model=model, trim=trim)
	reviews = ReviewUS.objects.filter(car__make=make, car__model=model, car__trim=trim).order_by('-created')
	context = {"form": form, "make": make, "model": model, "trim": trim, "reviews": reviews}
	return render(request, "reviews/us/car-select.html", context)


def year_select_us_view(request, make, model, trim, version):
	year = None
	if request.GET.get("submitted", None):
		form = forms.YearSelectUSForm(request.GET, make=make, model=model, trim=trim, version=version)
		if form.is_valid():
			year = form.cleaned_data['year']
			return redirect("reviews:car-us", make=make, model=model, trim=trim, version=version, year=year)
	else:
		form = forms.YearSelectUSForm(make=make, model=model, trim=trim, version=version)
	reviews = ReviewUS.objects.filter(car__make=make, car__model=model, car__trim=trim, car__version=version).order_by('-created')
	context = {"form": form, "make": make, "model": model, "trim": trim, "version": version, "reviews": reviews}
	return render(request, "reviews/us/car-select.html", context)


def car_us_view(request, make, model, trim, version, year, sort=None):
	car = CarUS.objects.get(make=make, model=model, trim=trim, version=version, year=year)
	review_users = ReviewUS.objects.filter(car=car).values_list('user',flat=True)

	if ListingUS.objects.filter(car=car):
		min_price = ListingUS.objects.filter(car=car).order_by('price')[0].price
		max_price = ListingUS.objects.filter(car=car).order_by('-price')[0].price
	else:
		min_price = None
		max_price = None

	if ReviewUS.objects.filter(car=car):
		total = 0
		total_rating = 0
		for review in ReviewUS.objects.filter(car=car):
			total_rating += review.rating * (1.5**review.vote_score)
			total += (1.5**review.vote_score)
		average_rating = round(total_rating/total,1)
		#average_rating = round(Review.objects.filter(car=car).aggregate(Avg('rating'))['rating__avg'],1)
	else:
		average_rating = None

	form = forms.ReviewUSForm(initial={'rating': ''})
	if request.method == 'POST':
		form = forms.ReviewUSForm(request.POST)
		if form.is_valid():
			review = form.save(commit=False)
			review.text = form.cleaned_data['text']
			review.title = form.cleaned_data['title']
			review.rating = form.cleaned_data['rating']
			review.car = car
			review.user = request.user
			review.save()
			messages.success(request, 'Your review has been published!')
			return redirect("reviews:car-us", make=make, model=model, trim=trim, version=version, year=year)

	if sort == None:
		reviews = ReviewUS.objects.filter(car=car).reverse()
	elif sort == 'best':
		reviews = ReviewUS.objects.filter(car=car).order_by('-vote_score')

	context = {"car": car,
	"average_rating": average_rating, 
	"form": form, 
	"review_users": review_users,
	"min_price": min_price,
	"max_price": max_price,
	"reviews": reviews,
	"sort": sort}

	return render(request, "reviews/us/car.html", context)