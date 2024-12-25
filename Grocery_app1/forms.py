from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Review

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment','email']
        widgets = {
     
            'comment': forms.Textarea(attrs={'id': 'comment', 'class': 'form-control custom-comment','placeholder': 'Enter your comment'}),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'class': 'form-control custom-email',
                'placeholder': 'Enter your email'
            }),
        }
