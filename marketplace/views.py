from django import forms
from django.db.models import Avg
from django.shortcuts import render, redirect
from num2words import num2words
from pathlib import Path
from reviews.forms import MakeSelectForm, ModelSelectForm, PlatformSelectForm, BodySelectForm, VersionSelectForm, YearsSelectForm
from reviews.models import Car
from .forms import ListingForm
from .models import Listing


def make_select_view(request):
	if request.GET.get("submitted", None):
		form = MakeSelectForm(request.GET)
		if form.is_valid():
			make = form.cleaned_data['make']
			return redirect("marketplace:model-select", make=make)
	else:
		form = MakeSelectForm()
	listings = Listing.objects.all().order_by('-created')
	context = {"form": form, "listings": listings}
	return render(request, "marketplace/carselect.html", context)


def model_select_view(request, make):
	model = None
	if request.GET.get("submitted", None):
		form = ModelSelectForm(request.GET, make=make)
		if form.is_valid():
			model = form.cleaned_data['model']
			return redirect("marketplace:platform-select", make=make, model=model)
	else:
		form = ModelSelectForm(make=make)
	listings = Listing.objects.filter(car__make=make).order_by('-created')
	context = {"form": form, "make": make, "listings": listings}
	return render(request, "marketplace/carselect.html", context)


def platform_select_view(request, make, model):
	platform = None
	if request.GET.get("submitted", None):
		form = PlatformSelectForm(request.GET, make=make, model=model)
		if form.is_valid():
			platform = form.cleaned_data['platform']
			return redirect("marketplace:body-select", make=make, model=model, platform=platform)       
	else:
		form = PlatformSelectForm(make=make, model=model)
	listings = Listing.objects.filter(car__make=make, car__model=model).order_by('-created')
	context = {"form": form, "make": make, "model": model, "listings": listings}
	return render(request, "marketplace/carselect.html", context)


def body_select_view(request, make, model, platform):
	body = None
	if request.GET.get("submitted", None):
		form = BodySelectForm(request.GET, make=make, model=model, platform=platform)
		if form.is_valid():
			body = form.cleaned_data['body']
			return redirect("marketplace:version-select", make=make, model=model, platform=platform, body=body)
	else:
		form = BodySelectForm(make=make, model=model, platform=platform)
	listings = Listing.objects.filter(car__make=make, car__model=model, car__platform=platform).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "listings": listings}
	return render(request, "marketplace/carselect.html", context)


def version_select_view(request, make, model, platform, body):
	version = None
	if request.GET.get("submitted", None):
		form = VersionSelectForm(request.GET, make=make, model=model, platform=platform, body=body)
		if form.is_valid():
			version = form.cleaned_data['version']
			return redirect("marketplace:years-select", make=make, model=model, platform=platform, body=body, version=version)       
	else:
		form = VersionSelectForm(make=make, model=model, platform=platform, body=body)
	listings = Listing.objects.filter(car__make=make, car__model=model, car__platform=platform, car__body=body).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "body": body, "listings": listings}
	return render(request, "marketplace/carselect.html", context)


def years_select_view(request, make, model, platform, body, version):
	years = None
	if request.GET.get("submitted", None):
		form = YearsSelectForm(request.GET, make=make, model=model, platform=platform, body=body, version=version)
		if form.is_valid():
			years = form.cleaned_data['years']
			return redirect("car-listings", make=make, years=years)
	else:
		form = YearsSelectForm(make=make, model=model, platform=platform, body=body, version=version)
	listings = Listing.objects.filter(car__make=make, car__model=model, car__platform=platform, car__body=body, car__version=version).order_by('-created')
	context = {"form": form, "make": make, "model": model, "platform": platform, "body": body, "version": version, "listings": listings}
	return render(request, "marketplace/carselect.html", context)

def car_listings_view(request, make, years):
	listings = Listing.objects.filter(car__make=make, car__years=years).order_by('-created')
	context = {"make": make, "years": years, "listings": listings}
	return render(request, "marketplace/carselect.html", context)


def new_listing_view(request, make, years):
	form = ListingForm(make=make, years=years)

	if request.method == 'POST':
		form = ListingForm(request.POST, request.FILES, make=make, years=years)
		if form.is_valid():
			listing = form.save(commit=False)
			listing.user = request.user
			listing.car = form.cleaned_data['car']
			listing.title = form.cleaned_data['title']
			listing.photo = form.cleaned_data['photo']
			listing.price = form.cleaned_data['price']
			listing.mileage = form.cleaned_data['mileage']
			listing.year = form.cleaned_data['year']
			listing.color = form.cleaned_data['color']
			listing.condition = form.cleaned_data['condition']
			listing.seller = form.cleaned_data['seller']
			listing.country = form.cleaned_data['country']
			listing.city = form.cleaned_data['city']
			listing.save()
			return redirect("car-listings", make=make, years=years)

	context = {"make": make, "years": years, "form": form}
	return render(request, "marketplace/newlisting.html", context)


def car_listing_view(request, make, years, listing_id):
	listing = Listing.objects.get(id=listing_id)
	return render(request, "marketplace/listing.html", {"listing": listing})