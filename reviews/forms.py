from django import forms
from .models import Car, CarUS, Review, ReviewUS, SuggestedPicture


def file_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Ops! Your image is larger than 1 MB.')


class MakeSelectForm(forms.Form):
	make = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

	def __init__(self, *args, **kwargs):
		super(MakeSelectForm, self).__init__(*args, **kwargs)
		qs = Car.objects.values_list('make',flat=True).distinct()
		choices = [(value, value) for value in qs]
		self.fields["make"].choices = choices


class ModelSelectForm(forms.Form):
    model = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        make = kwargs.pop("make", None)
        if not make:
            raise ValueError("Expected a 'make'")
        super(ModelSelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make).values_list('model',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["model"].choices = choices
        

class PlatformSelectForm(forms.Form):
    platform = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not model:
            raise ValueError("Expected a 'model'")
        super(PlatformSelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make, model=model).values_list('platform',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["platform"].choices = choices


class BodySelectForm(forms.Form):
    body = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        platform = kwargs.pop("platform", None)
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not platform:
            raise ValueError("Expected a 'platform'")
        super(BodySelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make, model=model, platform=platform).values_list('body_type',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["body"].choices = choices


class VersionSelectForm(forms.Form):
    version = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        body_type = kwargs.pop("body_type", None)
        platform = kwargs.pop("platform", None)
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not body_type:
            raise ValueError("Expected a 'body'")
        super(VersionSelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type).values_list('version',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["version"].choices = choices


class YearsSelectForm(forms.Form):
    years = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        version = kwargs.pop("version", None)
        body_type = kwargs.pop("body_type", None)
        platform = kwargs.pop("platform", None)
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not version:
            raise ValueError("Expected a 'version'")
        super(YearsSelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make, model=model, platform=platform, body_type=body_type, version=version).values_list('years',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["years"].choices = choices


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "text", "rating"]
        labels = {
            "text": ("Review"),
        }
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "text": forms.Textarea(attrs={'rows':5, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        ratings = [ (x+1,str(x+1)) for x in range(10) ]
        self.fields['rating'] = forms.ChoiceField(choices = [('','--')] + ratings)


class SuggestedPictureForm(forms.ModelForm):
    class Meta:
        model = SuggestedPicture
        fields = ["picture"]
        widgets = {
            "picture": forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


    ### AMERICAN DATABASE ###


class MakeSelectUSForm(forms.Form):
    make = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(MakeSelectUSForm, self).__init__(*args, **kwargs)
        qs = CarUS.objects.values_list('make',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["make"].choices = choices


class ModelSelectUSForm(forms.Form):
    model = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        make = kwargs.pop("make", None)
        if not make:
            raise ValueError("Expected a 'make'")
        super(ModelSelectUSForm, self).__init__(*args, **kwargs)
        qs = CarUS.objects.filter(make=make).values_list('model',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["model"].choices = choices
        

class TrimSelectUSForm(forms.Form):
    trim = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not model:
            raise ValueError("Expected a 'model'")
        super(TrimSelectUSForm, self).__init__(*args, **kwargs)
        qs = CarUS.objects.filter(make=make, model=model).values_list('trim',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["trim"].choices = choices


class VersionSelectUSForm(forms.Form):
    version = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        trim = kwargs.pop("trim", None)
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not trim:
            raise ValueError("Expected a 'trim'")
        super(VersionSelectUSForm, self).__init__(*args, **kwargs)
        qs = CarUS.objects.filter(make=make, model=model, trim=trim).values_list('version',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["version"].choices = choices


class YearSelectUSForm(forms.Form):
    year = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        version = kwargs.pop("version", None)
        trim = kwargs.pop("trim", None)
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not version:
            raise ValueError("Expected a 'version'")
        super(YearSelectUSForm, self).__init__(*args, **kwargs)
        qs = CarUS.objects.filter(make=make, model=model, trim=trim, version=version).values_list('year',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["year"].choices = choices


class ReviewUSForm(forms.ModelForm):
    class Meta:
        model = ReviewUS
        fields = ["title", "text", "rating"]
        labels = {
            "text": ("Review"),
        }
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "text": forms.Textarea(attrs={'rows':5, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewUSForm, self).__init__(*args, **kwargs)
        ratings = [ (x+1,str(x+1)) for x in range(10) ]
        self.fields['rating'] = forms.ChoiceField(choices = [('','--')] + ratings)