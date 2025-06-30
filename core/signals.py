# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class StudentRegisterForm(UserCreationForm):
    student_id = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('student_id', 'email', 'password1', 'password2')