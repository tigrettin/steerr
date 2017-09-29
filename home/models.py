from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from reviews.models import Car
from vote.models import VoteModel
import datetime


class Subscriptions(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	cars = models.ManyToManyField(Car, related_name='followers', blank=True)
	members = models.ManyToManyField('self', related_name='followers', symmetrical=False)

	def __str__(self):
		return str(self.user)


def file_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Ops! Your image is larger than 1 MB.')


class Opinion(VoteModel, models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	photo = models.ImageField(upload_to="static/home/images/", null=True, blank=True, validators=[file_size])
	created = models.DateTimeField()
	modified = models.DateTimeField()

	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(Opinion, self).save(*args, **kwargs)

	class Meta:
		ordering = ['created']

	def __str__(self):
		return str(self.user)