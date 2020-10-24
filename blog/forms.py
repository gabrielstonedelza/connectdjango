from django import forms
from .models import Project, ProjectFiles, ProjectIssues, Issues, FixProjectIssue, FeedBack, ContactUs


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': "let's hear from you"}))

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


class ProjectFilesForm(forms.ModelForm):
    code = forms.CharField(label="", widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Enter code for file", "id": "project_file_code",
               "name": "project_file_code"}))

    class Meta:
        model = ProjectFiles
        fields = ['file_name', 'code']


class ProjectFilesUpdateForm(forms.ModelForm):
    code = forms.CharField(label="", widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Enter code for file", "id": "project_file_update",
               "name": "project_file_update"}))

    class Meta:
        model = ProjectFiles
        fields = ['file_name', 'code']


class Project_Issue_Form(forms.ModelForm):
    issue = forms.CharField(label="", widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Enter issue here", "id": "issue_code",
               "name": "issue_code"}))

    class Meta:
        model = ProjectIssues
        fields = ['issue']


class FixForm(forms.ModelForm):
    fix = forms.CharField(label="", widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "fix.....", "id": "fix_code",
               "name": "fix_code"}))

    class Meta:
        model = ProjectIssues
        fields = ['fix']