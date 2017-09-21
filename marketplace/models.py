from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone
import datetime
from reviews.models import Car


def file_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Ops! Your image is larger than 1 MB.')


class Listing(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	car = models.ForeignKey(Car)
	title = models.CharField(max_length=50)
	description = models.TextField()
	photo = models.ImageField(upload_to="static/marketplace/images/", null=True, blank=False, validators=[file_size])
	price = models.IntegerField()
	mileage = models.IntegerField()
	
	YEAR_CHOICES = [(year, year) for year in range(datetime.datetime.now().year, 1970, -1)]

	COLOR_CHOICES = (
	('WE', 'White'),
	('BK', 'Black'),
	('SR', 'Silver'),
	('GY', 'Grey'),
	('RD', 'Red'),
	('BE', 'Blue'),
	('GN', 'Green'),
	('YW', 'Yellow'),
	('OE', 'Orange'),
	)

	CONDITION_CHOICES = (
		('N', 'New'),
		('U', 'Used'),
	)

	SELLER_CHOICES = (
		('P', 'Private seller'),
		('D', 'Dealer'),
	)

	year = models.IntegerField(choices=YEAR_CHOICES)
	color = models.CharField(max_length=2, choices=COLOR_CHOICES)
	condition = models.CharField(max_length=1, choices=CONDITION_CHOICES)
	seller = models.CharField(max_length=1, choices=SELLER_CHOICES)
	country = CountryField()
	city = models.CharField(max_length=50)

	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField()

	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(Listing, self).save(*args, **kwargs)

	class Meta:
		ordering = ['created']

	def __str__(self):
		return str(self.car) + " // " + str(self.user)