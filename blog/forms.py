from django import forms
from .models import Tutorial, Comments, FeedBack, ContactUs, BlogPost, ImproveTuto, ImproveTutoComments


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your feedbacks really help us a lot',"id":"feedform"}))

    class Meta:
        model = FeedBack
        fields = ['feedback']


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    subject = forms.CharField(label="",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'subject'}))
    message = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'enter your message'}))

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']


class TutorialForm(forms.ModelForm):
    tutorial_content = forms.CharField(label="",
                                       widget=forms.Textarea(attrs={"class": "form-control", "id": "tutorial_form"}))

    class Meta:
        model = Tutorial
        fields = ['title', 'tutorial_content', 'image']


class TutorialUpdateForm(forms.ModelForm):
    tutorial_content = forms.CharField(label="",
                                       widget=forms.Textarea(attrs={"class": "form-control", "id": "tutorial_form"}))

    class Meta:
        model = Tutorial
        fields = ['title', 'tutorial_content', 'image']


class CommentsForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", "id": "comment_form", "placeholder": "what do you think about this tutorial"}))

    class Meta:
        model = Comments
        fields = ['comment']


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "id": "blog_content"}))

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'blog_image']


class BlogUpdateForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "id": "blog_content"}))

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'blog_image']

class ImproveTutoForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "title"}))
    can_be_modified = forms.CharField(label="",
                                       widget=forms.Textarea(attrs={"class": "form-control", "id": "can_be_improved_form"}))

    improvement_or_change = forms.CharField(label="",
                                       widget=forms.Textarea(attrs={"class": "form-control", "id": "improvement_or_change_form"}))

    class Meta:
        model = ImproveTuto
        fields = ['title', 'can_be_modified', 'improvement_or_change']


class ImproveTutoCommentsForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", "id": "comment_form", "placeholder": "comment"}))

    class Meta:
        model = ImproveTutoComments
        fields = ['comment']