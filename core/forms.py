# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentRegisterForm(UserCreationForm):
    student_id = forms.CharField(
        max_length=7,
        min_length=7,
        label="Student ID",
        widget=forms.TextInput(attrs={
            'pattern': '[0-9]{7}',
            'title': 'Enter exactly 7 digits',
            'placeholder': 'Enter your 7-digit Student ID'
        })
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email'
    }))

    nickname = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the name everyone knows you'
        })
    )

    class Meta:
        model = User
        fields = ('student_id', 'nickname', 'email', 'password1', 'password2')

class StudentLoginForm(forms.Form):
    student_id = forms.CharField(
        max_length=7,
        min_length=7,
        label="Student ID",
        widget=forms.TextInput(attrs={
            'pattern': '[0-9]{7}',
            'title': 'Enter exactly 7 digits',
            'placeholder': 'Enter your 7-digit Student ID'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password'
        })
    )
