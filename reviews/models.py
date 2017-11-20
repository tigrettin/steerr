from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from vote.models import VoteModel
import os


def file_size(value):
	limit = 1 * 1024 * 1024
	if value.size > limit:
		raise ValidationError('Ops! Your image is larger than 1 MB.')


def update_filename(instance, filename):
	path = "static/reviews/images/cars/suggested/"
	str_car = []
	for i in str(instance.car):
		if i == "?" or i == " ":
			str_car.append("_")
		else:
			str_car.append(i)
	str_car = "".join(str_car)
	format = str_car + "_by" + str(instance.user.id) + ".jpg"
	return os.path.join(path, format)


class Car(models.Model):

	#Model Naming
	make = models.CharField(max_length=50, null=True, blank=True)
	model = models.CharField(max_length=50, null=True, blank=True)
	platform = models.CharField(max_length=50, null=True, blank=True) #ASLINDA "Model (platform) years"
	body = models.CharField(max_length=50, null=True, blank=True) #ASLINDA "Model body (platform) years"
	version = models.CharField(max_length=50, null=True, blank=True) #ASLINDA "Model version"
	years = models.CharField(max_length=75, null=True, blank=True) #ASLINDA "Model version (description) years"
	#FİLTRE BİTTİ
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
	brakes_abs = models.CharField(max_length=50, null=True, blank=True) #ASLINDA "ABS"
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
	to_100_kmph_sec = models.CharField(max_length=50, null=True, blank=True) #ASLINDA "0-100 kmph (sec)"
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

	photo = models.ImageField(upload_to="static/reviews/images/cars/", null=True, blank=True, validators=[file_size])

	def __str__(self):
		return str(self.make) + " " + str(self.version) + " (" + str(self.years_sold) + ")"

	def version1st(self):
		version1st = self.version.split(' ', 1)[0]
		return str(version1st)


class CarUS(models.Model):

	#Naming
	make = models.CharField(max_length=50, null=True, blank=True)
	model = models.CharField(max_length=50, null=True, blank=True)
	year = models.CharField(max_length=50, null=True, blank=True)
	trim = models.CharField(max_length=50, null=True, blank=True)
	version = models.CharField(max_length=50, null=True, blank=True) #ASLINDA "Description"
	#FİLTRE BİTTİ
	classification = models.CharField(max_length=50, null=True, blank=True) #ASLINDA "Class"
	url = models.CharField(max_length=125, null=True, blank=True)

	#Dimensions and Weight
	body_type = models.CharField(max_length=50, null=True, blank=True)
	length_in = models.CharField(max_length=50, null=True, blank=True)
	width_in = models.CharField(max_length=50, null=True, blank=True)
	height_in = models.CharField(max_length=50, null=True, blank=True)
	wheelbase_in = models.CharField(max_length=50, null=True, blank=True)
	curb_weight_lbs = models.CharField(max_length=50, null=True, blank=True)
	gross_weight_lbs = models.CharField(max_length=50, null=True, blank=True)
	maximum_payload_lbs = models.CharField(max_length=50, null=True, blank=True)
	maximum_towing_capacity_lbs = models.CharField(max_length=50, null=True, blank=True)

	#Engine and Transmission
	cylinders = models.CharField(max_length=50, null=True, blank=True)
	base_engine_size_l = models.CharField(max_length=50, null=True, blank=True)
	horsepower_hp = models.CharField(max_length=50, null=True, blank=True)
	horsepower_rpm = models.CharField(max_length=50, null=True, blank=True)
	torque_ft_lbs = models.CharField(max_length=50, null=True, blank=True)
	torque_rpm = models.CharField(max_length=50, null=True, blank=True)
	valves = models.CharField(max_length=50, null=True, blank=True)
	valve_timing = models.CharField(max_length=50, null=True, blank=True)
	cam_type = models.CharField(max_length=50, null=True, blank=True)
	drive_type = models.CharField(max_length=50, null=True, blank=True)
	transmission = models.CharField(max_length=50, null=True, blank=True)

	#Fuel
	engine_type = models.CharField(max_length=50, null=True, blank=True)
	fuel_type = models.CharField(max_length=50, null=True, blank=True)
	fuel_tank_capacity_gal = models.CharField(max_length=50, null=True, blank=True)
	epa_mileage_mpg = models.CharField(max_length=50, null=True, blank=True)
	range_miles = models.CharField(max_length=50, null=True, blank=True)

	#Interior Dimensions
	front_head_room_in = models.CharField(max_length=50, null=True, blank=True)
	front_hip_room_in = models.CharField(max_length=50, null=True, blank=True)
	front_leg_room_in = models.CharField(max_length=50, null=True, blank=True)
	front_shoulder_room_in = models.CharField(max_length=50, null=True, blank=True)
	rear_head_room_in = models.CharField(max_length=50, null=True, blank=True)
	rear_hip_room_in = models.CharField(max_length=50, null=True, blank=True)
	rear_leg_room_in = models.CharField(max_length=50, null=True, blank=True)
	rear_shoulder_room_in = models.CharField(max_length=50, null=True, blank=True)

	#Other Dimensions and Weight
	front_track_in = models.CharField(max_length=50, null=True, blank=True)
	rear_track_in = models.CharField(max_length=50, null=True, blank=True)
	ground_clearance_in = models.CharField(max_length=50, null=True, blank=True)
	angle_of_approach_degrees = models.CharField(max_length=50, null=True, blank=True)
	angle_of_departure_degrees = models.CharField(max_length=50, null=True, blank=True)
	turning_circle_ft = models.CharField(max_length=50, null=True, blank=True)
	drag_coefficient_cd = models.CharField(max_length=50, null=True, blank=True)
	epa_interior_volume_cu_ft = models.CharField(max_length=50, null=True, blank=True)
	cargo_capacity_cu_ft = models.CharField(max_length=50, null=True, blank=True)
	maximum_cargo_capacity_cu_ft = models.CharField(max_length=50, null=True, blank=True)
	suspension = models.CharField(max_length=50, null=True, blank=True)

	#Warranty
	basic = models.CharField(max_length=50, null=True, blank=True)
	drivetrain = models.CharField(max_length=50, null=True, blank=True)
	roadside = models.CharField(max_length=50, null=True, blank=True)
	rust = models.CharField(max_length=50, null=True, blank=True)
	free_maintenance = models.CharField(max_length=50, null=True, blank=True)
	hybrid_component = models.CharField(max_length=50, null=True, blank=True)
	ev_battery = models.CharField(max_length=50, null=True, blank=True)

	#Colors
	colors_exterior = models.CharField(max_length=150, null=True, blank=True)
	colors_interior = models.CharField(max_length=150, null=True, blank=True)
	colors_exterior_rgb = models.CharField(max_length=500, null=True, blank=True)
	colors_interior_rgb = models.CharField(max_length=500, null=True, blank=True)

	#Interior Features
	front_seats = models.CharField(max_length=500, null=True, blank=True)
	rear_seats = models.CharField(max_length=500, null=True, blank=True)
	power_features = models.CharField(max_length=500, null=True, blank=True)
	instrumentation = models.CharField(max_length=500, null=True, blank=True)
	convenience = models.CharField(max_length=500, null=True, blank=True)
	comfort = models.CharField(max_length=500, null=True, blank=True)
	memorized_settings = models.CharField(max_length=500, null=True, blank=True)
	in_car_entertainment = models.CharField(max_length=500, null=True, blank=True)
	telematics = models.CharField(max_length=500, null=True, blank=True)

	#Exterior Features
	roof_and_glass = models.CharField(max_length=500, null=True, blank=True)
	body = models.CharField(max_length=500, null=True, blank=True)
	truck_features = models.CharField(max_length=500, null=True, blank=True)
	tires_and_wheels = models.CharField(max_length=500, null=True, blank=True)
	doors = models.CharField(max_length=500, null=True, blank=True)
	towing_and_hauling = models.CharField(max_length=500, null=True, blank=True)

	#Safety
	safety_features = models.CharField(max_length=500, null=True, blank=True)

	#Optional Features
	packages = models.CharField(max_length=500, null=True, blank=True)
	exterior_options = models.CharField(max_length=500, null=True, blank=True)
	interior_options = models.CharField(max_length=500, null=True, blank=True)
	mechanical_options = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		trim1st = []
		for i in str(self.trim):
			if i != "-":
				trim1st.append(i)
			else:
				break
		trim1st = "".join(trim1st)
		return str(self.make) + " " + trim1st + "(" + str(self.year) + ")"


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
		return str(self.car) + " // " + str(self.user)


class ReviewUS(VoteModel, models.Model):
	car = models.ForeignKey(CarUS)
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
		return super(ReviewUS, self).save(*args, **kwargs)

	class Meta:
		ordering = ['created']
		unique_together = ('car', 'user',)

	def __str__(self):
		return str(self.car) + " // " + str(self.user)


class SuggestedPicture(models.Model):
	user = models.ForeignKey(User)
	car = models.ForeignKey(Car)
	picture = models.ImageField(upload_to=update_filename, null=True, blank=False, validators=[file_size])

	def __str__(self):
		return str(self.car) + " // " + str(self.user)