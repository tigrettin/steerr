from django.contrib.auth.models import User
from django import forms
from .models import Opinion

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ["username", "email", "password"]
		"""widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "password": forms.PasswordInput(attrs={'class': 'form-control'}),
            }"""


class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ["text", "photo"]
        labels = {
            "text": ("What do you think? Share"),
            "photo": ("Photo (< 1 MB):")
        }
        widgets = {
            "text": forms.Textarea(attrs={'rows':5, 'class': 'form-control'}),
        }