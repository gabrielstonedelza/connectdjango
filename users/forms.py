from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"username"}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"email"}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "password"}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "confirm password"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=100)

    class Meta:
        model = Profile
        fields = ['bio', 'name', 'profile_pic', 'your_facebook', 'your_instagram', 'your_twitter',
                  'your_youtube', 'your_medium', 'your_linkedin', 'your_github', 'your_organization']


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "old password"}))
    new_password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "new password"}))
    confirm_password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "confirm password"}))


