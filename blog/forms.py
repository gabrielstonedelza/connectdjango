from django import forms
from .models import Answers, Tutorial, Question, FeedBack, ContactUs


class QuestionForm(forms.ModelForm):
    question = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ['question', 'q_description']


class AnswerForm(forms.ModelForm):
    answer = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Answer goes here....', 'rows': '2', 'cols': '35', 'id': 'answerform',
               'name': 'answerform'}))

    class Meta:
        model = Answers
        fields = ['answer']


class TutorialForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tutorial_content = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Add tutorial here....', 'rows': '2', 'cols': '35', 'id': 'mytutorialform'}))

    class Meta:
        model = Tutorial
        fields = ['title', 'tutorial_content', 'make_private']


class TutorialUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tutorial_content = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Add tutorial here....', 'rows': '2', 'cols': '35', 'id': 'mytutorialform'}))

    class Meta:
        model = Tutorial
        fields = ['title', 'tutorial_content', 'make_private']


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
