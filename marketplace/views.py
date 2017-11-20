from django import forms
from django.db.models import Avg, Min
from django.shortcuts import render, redirect
from num2words import num2words
from pathlib import Path
from reviews.forms import MakeSelectForm, ModelSelectForm, PlatformSelectForm, BodySelectForm, VersionSelectForm, YearsSelectForm, MakeSelectUSForm, ModelSelectUSForm, TrimSelectUSForm, VersionSelectUSForm, YearSelectUSForm
from reviews.models import Car, CarUS
from .forms import ListingForm, ListingUSForm
from .models import Listing, ListingUS


def make_select_view(request):
	if request.GET.get("submitted", None):
		form = MakeSelectForm(request.GET)
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
								return redirect("marketplace:car-listings", make=make, years=years, body_type=body_type)
							else:
								return redirect("marketplace:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)
						else:
							return redirect("marketplace:version-select", make=make, model=model, platform=platform, body_type=body_type)
					else:
						return redirect("marketplace:body-select", make=make, model=model, platform=platform)
				else:
					return redirect("marketplace:platform-select", make=make, model=model)
			else:
				return redirect("marketplace:model-select", make=make)
	else:
		form = MakeSelectForm()
	listings = Listing.objects.all().order_by('-created')
	context = {"form": form, "listings": listings}
	return render(request, "marketplace/car-select.html", context)


def model_select_view(request, make):
	model = None
	if request.GET.get("submitted", None):
		form = ModelSelectForm(request.GET, make=make)
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
							return redirect("marketplace:car-listings", make=make, years=years, body_type=body_type)
						else:
							return redirect("marketplace:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)
					else:
						return redirect("marketplace:version-select", make=make, model=model, platform=platform, body_type=body_type)
				else:
					return redirect("marketplace:body-select", make=make, model=model, platform=platform)
			else:
				return redirect("marketplace:platform-select", make=make, model=model)
	else:
		form = ModelSelectForm(make=make)
	listings = Listing.objects.filter(car__make=make).order_by('-created')
	context = {"form": form, "make": make, "listings": listings}
	return render(request, "marketplace/car-select.html", context)


def platform_select_view(request, make, model):
	platform = None
	if request.GET.get("submitted", None):
		form = PlatformSelectForm(request.GET, make=make, model=model)
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
						return redirect("marketplace:car-listings", make=make, years=years, body_type=body_type)
					else:
						return redirect("marketplace:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)
				else:
					return redirect("marketplace:version-select", make=make, model=model, platform=platform, body_type=body_type)
			else:
				return redirect("marketplace:body-select", make=make, model=model, platform=platform)       
	else:
		form = PlatformSelectForm(make=make, model=model)
	listings = Listing.objects.filter(car__make=make, car__model=model).order_by('-created')
	context = {"form": form, "make": make, "model": model, "listings": listings}
	return render(request, "marketplace/car-select.html", context)


def body_select_view(request, make, model, platform):
	body_type = None
	if request.GET.get("submitted", None):
		form = BodySelectForm(request.GET, make=make, model=model, platform=platform)
		if form.is_valid():
			body_type = form.cleaned_data['body']
			versions = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type).values_list('version',flat=True).distinct()
			if len(versions) == 1:
				version = versions[0]
				yearss = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type, version=version).values_list('years',flat=True).distinct()
				if len(yearss) == 1:
					years = yearss[0]
					return redirect("marketplace:car-listings", make=make, years=years, body_type=body_type)
				else:
					return redirect("marketplace:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)
			else:
				return redirect("marketplace:version-select", make=make, model=model, platform=platform, body_type=body_type)
	else:
		form = BodySelectForm(make=make, model=model, platform=platform)
	listings = Listing.objects.filter(car__make=make, car__model=model, car__platform=platform).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "listings": listings}
	return render(request, "marketplace/car-select.html", context)


def version_select_view(request, make, model, platform, body_type):
	version = None
	if request.GET.get("submitted", None):
		form = VersionSelectForm(request.GET, make=make, model=model, platform=platform, body_type=body_type)
		if form.is_valid():
			version = form.cleaned_data['version']
			yearss = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type, version=version).values_list('years',flat=True).distinct()
			if len(yearss) == 1:
				years = yearss[0]
				return redirect("marketplace:car-listings", make=make, years=years, body_type=body_type)
			else:
				return redirect("marketplace:years-select", make=make, model=model, platform=platform, body_type=body_type, version=version)       
	else:
		form = VersionSelectForm(make=make, model=model, platform=platform, body_type=body_type)
	listings = Listing.objects.filter(car__make=make, car__model=model, car__platform=platform, car__body_type=body_type).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "body_type": body_type, "listings": listings}
	return render(request, "marketplace/car-select.html", context)


def years_select_view(request, make, model, platform, body_type, version):
	years = None
	if request.GET.get("submitted", None):
		form = YearsSelectForm(request.GET, make=make, model=model, platform=platform, body_type=body_type, version=version)
		if form.is_valid():
			years = form.cleaned_data['years']
			return redirect("marketplace:car-listings", make=make, years=years, body_type=body_type)
	else:
		form = YearsSelectForm(make=make, model=model, platform=platform, body_type=body_type, version=version)
	listings = Listing.objects.filter(car__make=make, car__model=model, car__platform=platform, car__body_type=body_type, car__version=version).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "body_type": body_type, "version": version, "listings": listings}
	return render(request, "marketplace/car-select.html", context)

def car_listings_view(request, make, years, body_type):
	if len(Car.objects.filter(make=make, years=years, body_type=body_type)) == 1:
		car = Car.objects.get(make=make, years=years, body_type=body_type)
	else:
		doors_min = Car.objects.filter(make=make, years=years, body_type=body_type).aggregate(Min('no_of_doors'))['no_of_doors__min']
		car = Car.objects.get(make=make, years=years, body_type=body_type, no_of_doors=doors_min)
	listings = Listing.objects.filter(car__make=make, car__years=years, car__body_type=body_type).order_by('-created')
	context = {"car": car, "listings": listings}
	return render(request, "marketplace/car-select.html", context)


def new_listing_view(request, make, years, body_type):
	form = ListingForm(make=make, years=years, body_type=body_type)

	if request.method == 'POST':
		form = ListingForm(request.POST, request.FILES, make=make, years=years, body_type=body_type)
		if form.is_valid():
			listing = form.save(commit=False)
			listing.user = request.user
			listing.car = form.cleaned_data['car']
			listing.title = form.cleaned_data['title']

			listing.photo1 = form.cleaned_data['photo1']
			listing.photo2 = form.cleaned_data['photo2']
			listing.photo3 = form.cleaned_data['photo3']
			listing.photo4 = form.cleaned_data['photo4']
			listing.photo5 = form.cleaned_data['photo5']

			listing.price = form.cleaned_data['price']
			listing.mileage = form.cleaned_data['mileage']
			listing.year = form.cleaned_data['year']
			listing.color = form.cleaned_data['color']
			listing.condition = form.cleaned_data['condition']
			listing.seller = form.cleaned_data['seller']
			listing.country = form.cleaned_data['country']
			listing.city = form.cleaned_data['city']
			listing.save()
			messages.success(request, 'Your listing has been published!')
			return redirect("marketplace:car-listings", make=make, years=years, body_type=body_type)

	context = {"form": form}
	return render(request, "marketplace/new-listing.html", context)


def car_listing_view(request, make, years, body_type, listing_id):
	listing = Listing.objects.get(id=listing_id)

	photos = []
	if listing.photo1:
		photos.append(listing.photo1)
	if listing.photo2:
		photos.append(listing.photo2)
	if listing.photo3:
		photos.append(listing.photo3)
	if listing.photo4:
		photos.append(listing.photo4)
	if listing.photo5:
		photos.append(listing.photo5)

	return render(request, "marketplace/listing.html", {"listing": listing, "photos": photos})


	### AMERICAN DATABASE ###


def make_select_us_view(request):
	if request.GET.get("submitted", None):
		form = MakeSelectUSForm(request.GET)
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
							return redirect("marketplace:car-us-listings", make=make, model=model, trim=trim, version=version, year=year)
						else:
							return redirect("marketplace:year-select-us", make=make, model=model, trim=trim, version=version)
					else:
						return redirect("marketplace:version-select-us", make=make, model=model, trim=trim)
				else:
					return redirect("marketplace:trim-select-us", make=make, model=model)
			else:
				return redirect("marketplace:model-select-us", make=make)
	else:
		form = MakeSelectUSForm()
	listings = ListingUS.objects.all().order_by('-created')
	context = {"form": form, "listings": listings}
	return render(request, "marketplace/us/car-select.html", context)


def model_select_us_view(request, make):
	model = None
	if request.GET.get("submitted", None):
		form = ModelSelectUSForm(request.GET, make=make)
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
						return redirect("marketplace:car-listings-us", make=make, model=model, trim=trim, version=version, year=year)
					else:
						return redirect("marketplace:year-select-us", make=make, model=model, trim=trim, version=version)
				else:
					return redirect("marketplace:version-select-us", make=make, model=model, trim=trim)
			else:
				return redirect("marketplace:trim-select-us", make=make, model=model)
	else:
		form = ModelSelectUSForm(make=make)
	listings = ListingUS.objects.filter(car__make=make).order_by('-created')
	context = {"form": form, "make": make, "listings": listings}
	return render(request, "marketplace/us/car-select.html", context)


def trim_select_us_view(request, make, model):
	trim = None
	if request.GET.get("submitted", None):
		form = TrimSelectUSForm(request.GET, make=make, model=model)
		if form.is_valid():
			trim = form.cleaned_data['trim']
			versions = CarUS.objects.filter(make=make, model=model, trim=trim).values_list('version',flat=True).distinct()
			if len(versions) == 1:
				version = versions[0]
				years = CarUS.objects.filter(make=make, model=model, trim=trim, version=version).values_list('year',flat=True).distinct()
				if len(years) == 1:
					year = years[0]
					return redirect("marketplace:car-listings-us", make=make, model=model, trim=trim, version=version, year=year)
				else:
					return redirect("marketplace:year-select-us", make=make, model=model, trim=trim, version=version)
			else:
				return redirect("marketplace:version-select-us", make=make, model=model, trim=trim)
	else:
		form = TrimSelectUSForm(make=make, model=model)
	listings = ListingUS.objects.filter(car__make=make, car__model=model).order_by('-created')
	context = {"form": form, "make": make, "model": model, "listings": listings}
	return render(request, "marketplace/us/car-select.html", context)


def version_select_us_view(request, make, model, trim):
	version = None
	if request.GET.get("submitted", None):
		form = VersionSelectUSForm(request.GET, make=make, model=model, trim=trim)
		if form.is_valid():
			version = form.cleaned_data['version']
			years = CarUS.objects.filter(make=make, model=model, trim=trim, version=version).values_list('year',flat=True).distinct()
			if len(years) == 1:
				year = years[0]
				return redirect("marketplace:car-listings-us", make=make, model=model, trim=trim, version=version, year=year)
			else:
				return redirect("marketplace:year-select-us", make=make, model=model, trim=trim, version=version)
	else:
		form = VersionSelectUSForm(make=make, model=model, trim=trim)
	listings = ListingUS.objects.filter(car__make=make, car__model=model, car__trim=trim).order_by('-created')
	context = {"form": form, "make": make, "model": model, "trim": trim, "listings": listings}
	return render(request, "marketplace/us/car-select.html", context)


def year_select_us_view(request, make, model, trim, version):
	year = None
	if request.GET.get("submitted", None):
		form = YearSelectUSForm(request.GET, make=make, model=model, trim=trim, version=version)
		if form.is_valid():
			year = form.cleaned_data['year']
			return redirect("marketplace:car-listings-us", make=make, model=model, trim=trim, version=version, year=year)
	else:
		form = YearSelectUSForm(make=make, model=model, trim=trim, version=version)
	listings = ListingUS.objects.filter(car__make=make, car__model=model, car__trim=trim, car__version=version).order_by('-created')
	context = {"form": form, "make": make, "model": model, "trim": trim, "version": version, "listings": listings}
	return render(request, "marketplace/us/car-select.html", context)


def car_listings_us_view(request, make, model, trim, version, year):
	car = CarUS.objects.get(make=make, model=model, trim=trim, version=version, year=year)
	listings = ListingUS.objects.filter(car__make=make, car__model=model, car__trim=trim, car__version=version, car__year=year).order_by('-created')
	context = {"car": car, "listings": listings}
	return render(request, "marketplace/us/car-select.html", context)


def new_listing_us_view(request, make, model, trim, version, year):
	form = ListingUSForm(make=make, model=model, trim=trim, version=version, year=year)

	if request.method == 'POST':
		form = ListingUSForm(request.POST, request.FILES, make=make, model=model, trim=trim, version=version, year=year)
		if form.is_valid():
			listing = form.save(commit=False)
			listing.user = request.user
			listing.car = form.cleaned_data['car']
			listing.title = form.cleaned_data['title']

			listing.photo1 = form.cleaned_data['photo1']
			listing.photo2 = form.cleaned_data['photo2']
			listing.photo3 = form.cleaned_data['photo3']
			listing.photo4 = form.cleaned_data['photo4']
			listing.photo5 = form.cleaned_data['photo5']
			
			listing.price = form.cleaned_data['price']
			listing.mileage = form.cleaned_data['mileage']
			listing.year = form.cleaned_data['year']
			listing.color = form.cleaned_data['color']
			listing.condition = form.cleaned_data['condition']
			listing.seller = form.cleaned_data['seller']
			listing.country = form.cleaned_data['country']
			listing.city = form.cleaned_data['city']
			messages.success(request, 'Your listing has been published!')
			listing.save()
			return redirect("marketplace:car-listings-us", make=make, model=model, trim=trim, version=version, year=year)

	context = {"form": form}
	return render(request, "marketplace/us/new-listing.html", context)


def car_listing_us_view(request, make, model, trim, version, year, listing_id):
	listing = ListingUS.objects.get(id=listing_id)

	photos = []
	if listing.photo1:
		photos.append(listing.photo1)
	if listing.photo2:
		photos.append(listing.photo2)
	if listing.photo3:
		photos.append(listing.photo3)
	if listing.photo4:
		photos.append(listing.photo4)
	if listing.photo5:
		photos.append(listing.photo5)

	return render(request, "marketplace/us/listing.html", {"listing": listing, "photos": photos})