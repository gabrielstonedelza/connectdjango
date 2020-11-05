from django import forms
from .models import Tutorial, Comments, FeedBack, BlogPost, ImproveTuto, ImproveTutoComments


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your feedbacks really help us a lot',"id":"feedform"}))

    class Meta:
        model = FeedBack
        fields = ['feedback']


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
        attrs={"class": "form-control", "id": "main_comment_form", "placeholder": "what do you think about this tutorial"}))

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
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "title of your improvement"}))
    can_be_modified = forms.CharField(label="",widget=forms.Textarea(attrs={"class": "form-control", "id": "can_be_improved_form","placeholder":"Which or part of this tutorial can be improved or changed?"}))

    improvement_or_change = forms.CharField(label="",
                                       widget=forms.Textarea(attrs={"class": "form-control", "id": "improvement_or_change_form","placeholder":"What is your modification?"}))

    class Meta:
        model = ImproveTuto
        fields = ['title', 'can_be_modified', 'improvement_or_change']


class ImproveTutoCommentsForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", "id": "comment_form", "placeholder": "comment"}))

    class Meta:
        model = ImproveTutoComments
        fields = ['comment']