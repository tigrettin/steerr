from django.contrib.auth.models import User
from django import forms
from .models import Opinion, Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            "email": forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('photo','country')
        labels = {
            "photo": ("Profile picture (< 1 MB)")
        }
        widgets = {
            "photo": forms.ClearableFileInput(attrs={'class': 'form-control'}),
            "country": forms.Select(attrs={'class':'form-control'})
        }


class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ["text", "photo"]
        labels = {
            "text": ("What do you think? Share"),
            "photo": ("Photo (< 1 MB)")
        }
        widgets = {
            "text": forms.Textarea(attrs={'rows':5, 'class': 'form-control'}),
        }