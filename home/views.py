from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView, View
from functools import reduce
from itertools import chain
from marketplace.models import Listing, ListingUS
from marketplace.forms import ListingForm, ListingUSForm
from reviews.models import Car, CarUS, Review, ReviewUS
from reviews.forms import ReviewForm, ReviewUSForm
from .forms import UserForm, UserUpdateForm, ProfileForm, OpinionForm
from .models import Opinion, Subscriptions
import operator


def feed(request):
	reviews = Review.objects.all()
	reviews_us = ReviewUS.objects.all()
	listings = Listing.objects.all()
	listings_us = ListingUS.objects.all()
	opinions = Opinion.objects.all()
	
	if not request.user.is_authenticated():
		feed = sorted(chain(reviews, reviews_us, listings, listings_us, opinions), key=lambda instance: instance.created)
	else:
		reviews_subs = []
		for review in reviews:
			if review.car in request.user.subscriptions.cars.all() or review.user.subscriptions in request.user.subscriptions.members.all() or review.user==request.user:
				reviews_subs.append(review)
		reviews_us_subs = []
		for review in reviews_us:
			if review.car in request.user.subscriptions.cars_us.all() or review.user.subscriptions in request.user.subscriptions.members.all() or review.user==request.user:
				reviews_us_subs.append(review)
		listings_subs = []
		for listing in listings:
			if listing.car in request.user.subscriptions.cars.all() or listing.user.subscriptions in request.user.subscriptions.members.all() or listing.user==request.user:
				listings_subs.append(listing)
		listings_us_subs = []
		for listing in listings_us:
			if listing.car in request.user.subscriptions.cars_us.all() or listing.user.subscriptions in request.user.subscriptions.members.all() or listing.user==request.user:
				listings_us_subs.append(listing)
		opinions_subs = []
		for opinion in opinions:
			if opinion.user.subscriptions in request.user.subscriptions.members.all() or opinion.user==request.user:
				opinions_subs.append(opinion)
			else:
				cars_subs = request.user.subscriptions.cars.all()
				cars_us_subs =request.user.subscriptions.cars_us.all()
				for car in chain(cars_subs, cars_us_subs):
					if car in cars_subs:
						if car.make.lower() in opinion.text.lower() and car.version1st().lower() in opinion.text.lower():
							opinions_subs.append(opinion)
							break
					elif car in cars_us_subs:
						if car.make.lower() in opinion.text.lower() and car.model.lower() in opinion.text.lower():
							opinions_subs.append(opinion)
							break
		feed = sorted(chain(reviews_subs, reviews_us_subs, listings_subs, listings_us_subs, opinions_subs), key=lambda instance: instance.created)

	form = OpinionForm()
	if request.method == 'POST':
		form = OpinionForm(request.POST, request.FILES)
		if form.is_valid():
			opinion = form.save(commit=False)
			opinion.text = form.cleaned_data['text']
			opinion.photo = form.cleaned_data['photo']
			opinion.user = request.user
			opinion.save()
			return redirect("home:feed")

	context = {
	"feed": feed,
	"reviews": reviews,
	"reviews_us": reviews_us,
	"listings": listings,
	"listings_us": listings_us,
	"opinions": opinions,
	"form": form
	}

	return render(request, "home/feed.html", context)


def search(request):
	reviews = Review.objects.all()
	reviews_us = ReviewUS.objects.all()
	listings = Listing.objects.all()
	listings_us = ListingUS.objects.all()
	opinions = Opinion.objects.all()
	members = User.objects.all()

	query = request.GET.get('q')
	if query and query.strip():
		if query[0] == "@":
			search_results = User.objects.filter(username__icontains=query[1:])
		else:
			query_list = query.split()		
			opinion_results = Opinion.objects.filter(reduce(operator.and_,(Q(text__icontains=q) for q in query_list)))
			review_results = Review.objects.filter(reduce(operator.and_,(Q(text__icontains=q) for q in query_list)) | 
													reduce(operator.and_,(Q(title__icontains=q) for q in query_list)))
			review_us_results = ReviewUS.objects.filter(reduce(operator.and_,(Q(text__icontains=q) for q in query_list)) | 
													reduce(operator.and_,(Q(title__icontains=q) for q in query_list)))
			listing_results = Listing.objects.filter(reduce(operator.and_,(Q(description__icontains=q) for q in query_list)) | 
													reduce(operator.and_,(Q(title__icontains=q) for q in query_list)))
			listing_us_results = ListingUS.objects.filter(reduce(operator.and_,(Q(description__icontains=q) for q in query_list)) | 
													reduce(operator.and_,(Q(title__icontains=q) for q in query_list)))
			search_results = sorted(chain(opinion_results, review_results, review_us_results, listing_results, listing_us_results), key=lambda instance: instance.created)
	else:
		search_results = None

	context = {
	"search_results": search_results,
	"reviews": reviews,
	"reviews_us": reviews_us,
	"listings": listings,
	"listings_us": listings_us,
	"opinions": opinions,
	"members": members
	}

	return render(request, "home/search.html", context)


def content_vote(request, username, category, content_id):
	member = User.objects.get(username=username)

	if category == "opinions":
		opinion = Opinion.objects.get(id=content_id)
		if opinion.user != request.user:
			if "vote-up" in request.GET:
				opinion.votes.up(request.user.id)
			elif "vote-down" in request.GET:
				opinion.votes.down(request.user.id)
		if request.GET.get("member", None):
			return redirect("home:member", member.username)
		else:
			return redirect("home:feed")

	elif category == "reviews":
		review = Review.objects.get(id=content_id)
		if review.user != request.user:
			if "vote-up" in request.GET:
				review.votes.up(request.user.id)
			elif "vote-down" in request.GET:
				review.votes.down(request.user.id)
		return redirect("reviews:car", make=review.car.make, years=review.car.years, body_type=review.car.body_type)

	elif category == "reviews_us":
		review = ReviewUS.objects.get(id=content_id)
		if review.user != request.user:
			if "vote-up" in request.GET:
				review.votes.up(request.user.id)
			elif "vote-down" in request.GET:
				review.votes.down(request.user.id)
		return redirect("reviews:car-us", make=review.car.make, model=review.car.model, trim=review.car.trim, version=review.car.version, year=review.car.year)


def content_update(request, username, category, content_id):
	member = User.objects.get(username=username)

	if category == "opinions":		
		opinion = Opinion.objects.get(id=content_id)
		form = OpinionForm(request.POST or None, request.FILES or None, instance=opinion)
		if form.is_valid():
			form.save()
			messages.success(request, 'Opinion updated.')
			return redirect("home:member", member.username)

	elif category == "reviews":
		review = Review.objects.get(id=content_id)
		form = ReviewForm(request.POST or None, instance=review)
		if form.is_valid():
			form.save()
			messages.success(request, 'Review updated.')
			return redirect("home:member", member.username)

	elif category == "reviews_us":
		review = ReviewUS.objects.get(id=content_id)
		form = ReviewUSForm(request.POST or None, instance=review)
		if form.is_valid():
			form.save()
			messages.success(request, 'Review updated.')
			return redirect("home:member", member.username)

	elif category == "listings":
		listing = Listing.objects.get(id=content_id)
		form = ListingForm(request.POST or None, request.FILES or None, make=listing.car.make, years=listing.car.years, body_type=listing.car.body_type, instance=listing)
		if form.is_valid():
			form.save()
			messages.success(request, 'Listing updated.')
			return redirect("home:member", member.username)

	elif category == "listings_us":
		listing = ListingUS.objects.get(id=content_id)
		form = ListingUSForm(request.POST or None, request.FILES or None, make=listing.car.make, model=listing.car.model, trim=listing.car.trim, version=listing.car.version, year=listing.car.year, instance=listing)
		if form.is_valid():
			form.save()
			messages.success(request, 'Listing updated.')
			return redirect("home:member", member.username)

	context = {
	"member": member,
	"form": form,
	"category": category
	}

	return render(request, "home/update.html", context)


def content_confirm(request, username, category, content_id):
	member = User.objects.get(username=username)

	if category == "opinions":
		content = Opinion.objects.get(id=content_id)
	elif category == "reviews":
		content = Review.objects.get(id=content_id)
	elif category == "reviews_us":
		content = ReviewUS.objects.get(id=content_id)
	elif category == "listings":
		content = Listing.objects.get(id=content_id)
	elif category == "listings_us":
		content = ListingUS.objects.get(id=content_id)

	context = {
	"member": member,
	"content": content,
	"category": category
	}

	return render(request, "home/confirmation.html", context)


def content_delete(request, username, category, content_id):
	member = User.objects.get(username=username)

	if category == "opinions":
		Opinion.objects.filter(id=content_id).delete()
		messages.success(request, 'Opinion deleted.')
	elif category == "reviews":
		Review.objects.filter(id=content_id).delete()
		messages.success(request, 'Review deleted.')
	elif category == "reviews_us":
		ReviewUS.objects.filter(id=content_id).delete()
		messages.success(request, 'Review deleted.')
	elif category == "listings":
		Listing.objects.filter(id=content_id).delete()
		messages.success(request, 'Listing deleted.')
	elif category == "listings_us":
		ListingUS.objects.filter(id=content_id).delete()
		messages.success(request, 'Listing deleted.')

	return redirect("home:member", member.username)


class UserFormView(View):
	form_class = UserForm
	template_name = "registration/registration_form.html"

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {"form": form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user.set_password(password)
			user.save()

			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect("home:feed")

		return render(request, self.template_name, {"form": form})

	def logout_view(request):
		logout(request)
		return redirect("home:feed")


def member_view(request, username):
	member = User.objects.get(username=username)
	reviews = Review.objects.filter(user__username=username)
	reviews_us = ReviewUS.objects.filter(user__username=username)
	listings = Listing.objects.filter(user__username=username)
	listings_us = ListingUS.objects.filter(user__username=username)
	opinions = Opinion.objects.filter(user__username=username)
	feed = sorted(chain(reviews, reviews_us, listings, listings_us, opinions), key=lambda instance: instance.created)

	form = OpinionForm()
	if request.method == 'POST':
		form = OpinionForm(request.POST, request.FILES)
		if form.is_valid():
			opinion = form.save(commit=False)
			opinion.text = form.cleaned_data['text']
			opinion.photo = form.cleaned_data['photo']
			opinion.user = request.user
			opinion.save()
			return redirect("home:member", member.username)

	context = {
	"member": member,
	"feed": feed,
	"reviews": reviews,
	"reviews_us": reviews_us,
	"listings": listings,
	"listings_us": listings_us,
	"opinions": opinions,
	"form": form
	}

	return render(request, "home/member.html", context)


def member_subscribe(request, username):
	member = User.objects.get(username=username)

	follower_subs, created = Subscriptions.objects.get_or_create(user=request.user)
	followed_subs, created = Subscriptions.objects.get_or_create(user=member)

	if follower_subs != followed_subs:
		if "subscribe" in request.GET:
			follower_subs.members.add(followed_subs)
		elif "unsubscribe" in request.GET:
			follower_subs.members.remove(followed_subs)

	return redirect("home:member", username)


def member_edit(request, username):
	member = User.objects.get(username=username)

	userupdateform = UserUpdateForm(request.POST or None, instance=member)
	profileform = ProfileForm(request.POST or None, request.FILES or None, instance=member.profile)
	if userupdateform.is_valid() and profileform.is_valid():
		member.set_password(member.password)
		userupdateform.save()
		profileform.save()
		messages.success(request, 'Profile updated.')
		return redirect("home:member", member.username)

	context = {
	"member": member,
	"userupdateform": userupdateform,
	"profileform": profileform
	}

	return render(request, "home/member-edit.html", context)