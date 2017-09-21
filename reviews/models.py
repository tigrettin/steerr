from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
#from home.models import Subscriptions
from vote.models import VoteModel


class Car(models.Model):

	#Model Naming
	make = models.CharField(max_length=50, null=True, blank=True)
	model = models.CharField(max_length=50, null=True, blank=True)
	platform = models.CharField(max_length=50, null=True, blank=True)
	body = models.CharField(max_length=50, null=True, blank=True)
	version = models.CharField(max_length=50, null=True, blank=True)
	years = models.CharField(max_length=50, null=True, blank=True)
	# FİLTRE BİTTİ
	source_of_data = models.CharField(max_length=50, null=True, blank=True)
	years_sold = models.CharField(max_length=50, null=True, blank=True)
	sold_in_europe = models.CharField(max_length=50, null=True, blank=True)
	car_classification = models.CharField(max_length=50, null=True, blank=True)

	#Body Data
	body_type = models.CharField(max_length=50, null=True, blank=True)
	no_of_doors = models.CharField(max_length=50, null=True, blank=True)
	no_of_seats = models.CharField(max_length=50, null=True, blank=True)
	engine_place = models.CharField(max_length=50, null=True, blank=True)
	drivetrain = models.CharField(max_length=50, null=True, blank=True)	

	#Engine Data
	cylinders = models.CharField(max_length=50, null=True, blank=True)
	displacement_cm3 = models.CharField(max_length=50, null=True, blank=True)
	power_kw = models.CharField(max_length=50, null=True, blank=True)
	power_ps = models.CharField(max_length=50, null=True, blank=True)
	power_rpm = models.CharField(max_length=50, null=True, blank=True)
	torque_nm = models.CharField(max_length=50, null=True, blank=True)
	torque_rpm = models.CharField(max_length=50, null=True, blank=True)
	bore_stroke_mm = models.CharField(max_length=50, null=True, blank=True)
	compression_ratio = models.CharField(max_length=50, null=True, blank=True)
	valves_per = models.CharField(max_length=50, null=True, blank=True)
	crankshaft = models.CharField(max_length=50, null=True, blank=True)
	fuel_injection = models.CharField(max_length=50, null=True, blank=True)
	supercharger = models.CharField(max_length=50, null=True, blank=True)
	catalytic = models.CharField(max_length=50, null=True, blank=True)
	manual = models.CharField(max_length=50, null=True, blank=True)
	automatic = models.CharField(max_length=50, null=True, blank=True)

	#Drivetrain Data
	suspension_front = models.CharField(max_length=50, null=True, blank=True)
	suspension_rear = models.CharField(max_length=50, null=True, blank=True)
	assisted = models.CharField(max_length=50, null=True, blank=True)
	turning_circle_m = models.CharField(max_length=50, null=True, blank=True)
	brakes_front = models.CharField(max_length=50, null=True, blank=True)
	brakes_rear = models.CharField(max_length=50, null=True, blank=True)
	brakes_abs = models.CharField(max_length=50, null=True, blank=True) # ASLINDA "ABS"
	esp = models.CharField(max_length=50, null=True, blank=True)
	tire_size = models.CharField(max_length=50, null=True, blank=True)
	tire_size_rear = models.CharField(max_length=50, null=True, blank=True)

	#Body Data 2
	wheel_base_mm = models.CharField(max_length=50, null=True, blank=True)
	track_front_mm = models.CharField(max_length=50, null=True, blank=True)
	track_rear_mm = models.CharField(max_length=50, null=True, blank=True)
	length_mm = models.CharField(max_length=50, null=True, blank=True)
	width_mm = models.CharField(max_length=50, null=True, blank=True)
	height_mm = models.CharField(max_length=50, null=True, blank=True)
	curb_weight_kg = models.CharField(max_length=50, null=True, blank=True)
	gross_weight_kg = models.CharField(max_length=50, null=True, blank=True)
	load_kg = models.CharField(max_length=50, null=True, blank=True)
	stutzlast_kg = models.CharField(max_length=50, null=True, blank=True)
	roof_load_kg = models.CharField(max_length=50, null=True, blank=True)
	cargo_space_litres = models.CharField(max_length=50, null=True, blank=True)
	tow_weight_kg = models.CharField(max_length=50, null=True, blank=True)
	gas_tank_litres = models.CharField(max_length=50, null=True, blank=True)

	#Performance Data
	to_100_kmph_sec = models.CharField(max_length=50, null=True, blank=True) # ASLINDA "0-100 kmph (sec)"
	max_speed_kmh = models.CharField(max_length=50, null=True, blank=True)
	fuel_eff_l100km = models.CharField(max_length=50, null=True, blank=True)
	fuel_eff_city_l100km = models.CharField(max_length=50, null=True, blank=True)
	fuel_eff_highway = models.CharField(max_length=50, null=True, blank=True)
	engine_type = models.CharField(max_length=50, null=True, blank=True)
	fuel_type = models.CharField(max_length=50, null=True, blank=True)
	co2_gkm = models.CharField(max_length=50, null=True, blank=True)
	co2_efficiency_class = models.CharField(max_length=50, null=True, blank=True)
	pollution_class = models.CharField(max_length=50, null=True, blank=True)
	base_price_in_germany = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return str(self.make) + " " + str(self.years)

	def version1st(self):
		version1st = self.version.split(' ', 1)[0]
		return str(version1st)


class Review(VoteModel, models.Model):
	car = models.ForeignKey(Car)
	title = models.CharField(max_length=50)
	text = models.TextField()
	rating = models.IntegerField(default=5, validators=[MaxValueValidator(10), MinValueValidator(1)])
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField()

	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(Review, self).save(*args, **kwargs)

	class Meta:
		ordering = ['created']
		unique_together = ('car', 'user',)

	def __str__(self):
		return str(self.car)