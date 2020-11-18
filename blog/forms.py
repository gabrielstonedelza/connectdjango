from django import forms
from .models import  FeedBack


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your feedbacks really help us a lot',"id":"feedform"}))

    class Meta:
        model = FeedBack
        fields = ['feedback']

