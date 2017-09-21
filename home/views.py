from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from itertools import chain
from marketplace.models import Listing
from reviews.models import Review
from .forms import UserForm, OpinionForm
from .models import Opinion, Subscriptions


def feed(request):
	reviews = Review.objects.all()
	listings = Listing.objects.all()
	opinions = Opinion.objects.all()
	
	if not request.user.is_authenticated():
		feed = sorted(chain(reviews, listings, opinions), key=lambda instance: instance.created)
	else:
		reviews_subs = []
		for review in reviews:
			if review.car in request.user.subscriptions.cars.all() or review.user.subscriptions in request.user.subscriptions.members.all():
				reviews_subs.append(review)
		listings_subs = []
		for listing in listings:
			if listing.car in request.user.subscriptions.cars.all() or listing.user.subscriptions in request.user.subscriptions.members.all():
				listings_subs.append(listing)
		opinions_subs = []
		for opinion in opinions:
			if opinion.user.subscriptions in request.user.subscriptions.members.all():
				opinions_subs.append(opinion)
			else:
				for car in request.user.subscriptions.cars.all():
					if car.make.lower() in opinion.text.lower() and car.version1st().lower() in opinion.text.lower():
						opinions_subs.append(opinion)
						break
		feed = sorted(chain(reviews_subs, listings_subs, opinions_subs), key=lambda instance: instance.created)

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
	"listings": listings,
	"opinions": opinions,
	"form": form
	}

	return render(request, "home/feed.html", context)


def opinion_vote(request, username, opinion_id):
	member = User.objects.get(username=username)
	opinion = Opinion.objects.get(id=opinion_id)

	if opinion.user != request.user:
		if "vote-up" in request.GET:
			opinion.votes.up(request.user.id)
		elif "vote-down" in request.GET:
			opinion.votes.down(request.user.id)

	if request.GET.get("member", None):
		return redirect("home:member", member.username)
	else:
		return redirect("home:feed")


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
	listings = Listing.objects.filter(user__username=username)
	opinions = Opinion.objects.filter(user__username=username)
	feed = sorted(chain(reviews, listings, opinions), key=lambda instance: instance.created)

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
	"listings": listings,
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