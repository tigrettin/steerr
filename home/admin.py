from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Subscriptions, Opinion


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class SubscriptionsInline(admin.StackedInline):
    model = Subscriptions
    can_delete = False
    verbose_name_plural = 'Subscriptions'


class CustomUserAdmin(UserAdmin):
    inlines = (SubscriptionsInline, ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Opinion)