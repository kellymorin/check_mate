from django.contrib.auth.models import User
from django import forms
from check_mate.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ("project_name", "project_description")