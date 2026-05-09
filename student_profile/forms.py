from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Profile

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': _('Username'),
            'email': _('Email'),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone',
            'department',
            'location',
            'major',
            'interests',
            'skills',
            'profile_image'
        ]
        labels = {
            'phone': _('Phone'),
            'department': _('Department'),
            'location': _('Location'),
            'major': _('Major'),
            'interests': _('Interests'),
            'skills': _('Skills'),
            'profile_image': _('Profile Image'),
        }
