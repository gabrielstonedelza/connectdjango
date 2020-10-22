from django import forms
from .models import  Project, ProjectFiles, ProjectIssues, Issues, FeedBack, ContactUs


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "let's hear from you"}))

    class Meta:
        model = FeedBack
        fields = ['feedback']


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    subject = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'subject'}))
    message = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'enter your message'}))

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']

        
class ProjectFilesForm(forms.ModelForm):

    class Meta:
        model = ProjectFiles
        fields = ['']
