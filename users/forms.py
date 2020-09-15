from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Group, GroupPost, GroupAdminMsg, Comments


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
        fields = ['bio', 'name', 'profile_pic', 'cover_pic', 'your_facebook', 'your_instagram', 'your_twitter',
                  'your_youtube', 'your_medium', 'your_linkedin']


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "old password"}))
    new_password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "new password"}))
    confirm_password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "confirm password"}))


class GroupUpdateForm(forms.ModelForm):
    group_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(label='')
    group_description = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Group
        fields = ['group_name', 'logo', 'group_description']


class GroupPostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'grouppostform'}))

    class Meta:
        model = GroupPost
        fields = ['title', 'content', 'photo']


class CreateNewGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'logo', 'group_description']


class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = GroupAdminMsg
        fields = ['title', 'message']


class CommentsForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Comments goes here....', 'rows': '1', 'cols': '50', 'id': 'group_post_comment_form',
               'name': 'group_post_comment_form', 'class': 'form-control mb-2 mr-sm-2'}))

    class Meta:
        model = Comments
        fields = ['comment']
