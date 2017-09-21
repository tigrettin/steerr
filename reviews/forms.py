from django import forms
from .models import Car, Review


class MakeSelectForm(forms.Form):
	make = forms.ChoiceField()

	def __init__(self, *args, **kwargs):
		super(MakeSelectForm, self).__init__(*args, **kwargs)
		qs = Car.objects.values_list('make',flat=True).distinct()
		choices = [(value, value) for value in qs]
		self.fields["make"].choices = choices


class ModelSelectForm(forms.Form):
    model = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        make = kwargs.pop("make", None)
        if not make:
            raise ValueError("Expected a 'make'")
        super(ModelSelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make).values_list('model',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["model"].choices = choices
        

class PlatformSelectForm(forms.Form):
    platform = forms.ChoiceField()

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
    body = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        platform = kwargs.pop("platform", None)
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not platform:
            raise ValueError("Expected a 'platform'")
        super(BodySelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make, model=model, platform=platform).values_list('body',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["body"].choices = choices


class VersionSelectForm(forms.Form):
    version = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        body = kwargs.pop("body", None)
        platform = kwargs.pop("platform", None)
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not body:
            raise ValueError("Expected a 'body'")
        super(VersionSelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make, model=model, platform=platform, body=body).values_list('version',flat=True).distinct()
        choices = [(value, value) for value in qs]
        self.fields["version"].choices = choices


class YearsSelectForm(forms.Form):
    years = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        version = kwargs.pop("version", None)
        body = kwargs.pop("body", None)
        platform = kwargs.pop("platform", None)
        model = kwargs.pop("model", None)
        make = kwargs.pop("make", None)
        if not version:
            raise ValueError("Expected a 'version'")
        super(YearsSelectForm, self).__init__(*args, **kwargs)
        qs = Car.objects.filter(make=make, model=model, platform=platform, body=body, version=version).values_list('years',flat=True).distinct()
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