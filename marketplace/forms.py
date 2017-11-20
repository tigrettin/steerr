from django import forms
from django.forms import ModelChoiceField
from django.utils import timezone
from reviews.models import Car, CarUS
from .models import Listing, ListingUS


class MyModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s (%s doors)" % (obj, obj.no_of_doors)


class ListingForm(forms.ModelForm):

	class Meta:
		model = Listing
		localized_fields = '__all__'
		exclude = ['user', 'modified']
		labels = {
			"price": ("Price (€)"),
			"mileage": ("Mileage (km)"),
		}
		widgets = {
			"title": forms.TextInput(attrs={'class': 'form-control'}),
			"description": forms.Textarea(attrs={'rows':5, 'class': 'form-control'}),
			"price": forms.NumberInput(attrs={'class': 'form-control'}),
			"mileage": forms.NumberInput(attrs={'class': 'form-control'}),
			"year": forms.Select(attrs={'class': 'form-control'}),
			"color": forms.Select(attrs={'class': 'form-control'}),
			"condition": forms.Select(attrs={'class': 'form-control'}),
			"seller": forms.Select(attrs={'class': 'form-control'}),
			"country": forms.Select(attrs={'class': 'form-control'}),
			"city": forms.TextInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		make = kwargs.pop('make')
		years = kwargs.pop('years')
		body_type = kwargs.pop('body_type')

		if str(years)[-3:] == " ??":
			max_year = timezone.now().year
			min_year = 1970
		else:
			if not "_" in str(years)[-4:] and not "?" in str(years)[-4:]:
				max_year = int(str(years)[-4:])
			else:
				max_year = timezone.now().year

			if not "?" in str(years)[:-5]:
				if not "?" in str(years)[-4:]:
					min_year = int(str(years)[-10:-5])
				else:
					min_year = int(str(years)[-8:-3])
			else:
				min_year = 1970
		
		super(ListingForm, self).__init__(*args, **kwargs)
		year_choices = [ (x, x) for x in range(min_year, max_year+1) ]
		self.fields['year'].choices = year_choices
		if len(Car.objects.filter(make=make, years=years, body_type=body_type)) == 1:
			self.fields['car'] = ModelChoiceField(
				queryset = Car.objects.filter(make=make, years=years, body_type=body_type),
				initial={'make': make},
				widget=forms.Select(attrs={'class':'form-control'})
			)
		else:
			self.fields['car'] = MyModelChoiceField(
				queryset = Car.objects.filter(make=make, years=years, body_type=body_type),
				initial={'make': make},
				widget=forms.Select(attrs={'class':'form-control'})
			)


class ListingUSForm(forms.ModelForm):

	class Meta:
		model = ListingUS
		localized_fields = '__all__'
		exclude = ['user', 'modified']
		labels = {
			"price": ("Price ($)"),
			"mileage": ("Mileage (mi)"),
			"city": ("State")
		}
		widgets = {
			"title": forms.TextInput(attrs={'class': 'form-control'}),
			"description": forms.Textarea(attrs={'rows':5, 'class': 'form-control'}),
			"price": forms.NumberInput(attrs={'class': 'form-control'}),
			"mileage": forms.NumberInput(attrs={'class': 'form-control'}),
			"year": forms.Select(attrs={'class': 'form-control'}),
			"color": forms.Select(attrs={'class': 'form-control'}),
			"condition": forms.Select(attrs={'class': 'form-control'}),
			"seller": forms.Select(attrs={'class': 'form-control'}),
			"country": forms.Select(attrs={'class': 'form-control'}),
			"city": forms.TextInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		make = kwargs.pop('make')
		model = kwargs.pop('model')
		trim = kwargs.pop('trim')
		version = kwargs.pop('version')
		year = kwargs.pop('year')
		
		super(ListingUSForm, self).__init__(*args, **kwargs)
		self.fields['year'].initial = year
		self.fields['country'].initial = 'US'
		self.fields['car'] = ModelChoiceField(
				queryset = CarUS.objects.filter(make=make, model=model, trim=trim, version=version, year=year),
				initial={'make': make},
				widget=forms.Select(attrs={'class':'form-control'})
			)