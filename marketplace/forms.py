from django import forms
from django.forms import ModelChoiceField
from reviews.models import Car
from .models import Listing


class MyModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s (%s doors)" % (obj.make, obj.years, obj.no_of_doors)


class ListingForm(forms.ModelForm):

	class Meta:
		model = Listing
		localized_fields = '__all__'
		exclude = ['user', 'modified']
		labels = {
			"price": ("Price ($)"),
			"photo": ("Photo (< 1 MB)"),
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
		max_year = int(str(years)[-4:])
		min_year = int(str(years)[-10:-5])
		
		super(ListingForm, self).__init__(*args, **kwargs)
		year_choices = [ (x, x) for x in range(min_year, max_year+1) ]
		self.fields['year'].choices = year_choices
		self.fields['car'] = MyModelChoiceField(
			queryset = Car.objects.filter(make=make, years=years),
			initial={'make': make},
			widget=forms.Select(attrs={'class':'form-control'})
		)