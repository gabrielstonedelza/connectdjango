from django import forms
from .models import  FeedBack, Blog, Comments


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your feedbacks really help us a lot',"id":"feedform"}))

    class Meta:
        model = FeedBack
        fields = ['feedback']


class BlogForm(forms.ModelForm):
    title = forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"enter blog title"}))
    subtitle = forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":" subtitle"}))
    blog_content = forms.CharField(label="",widget=forms.Textarea(attrs="class":"form-control","placeholder":"blog content","id":"my_blog_content"))

    class Meta:
        model = Blog
        fields = ['title','subtitle','blog_pic','blog_content']

class CommentsForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'comment....', 'id': 'commentform'}))

    class Meta:
        model = Comments
        fields = ['comment']