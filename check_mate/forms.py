from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django import forms

from check_mate.models import *

# TODO: Add docstrings to all methods

class LogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=("username", "password")


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ("project_name", "project_description")


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ("ticket_name", "ticket_description", "ticket_due", "ticket_assigned_user")
        widgets = {
            "ticket_due": forms.DateInput(attrs={"type": "date"})
        }

class TicketStatusForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ("ticket_status",)

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("task_name", "task_description", "task_due", "task_assigned_user")
        widgets = {
            "task_due": forms.DateInput(attrs={"type": "date"})
        }

class TaskStatusForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("task_status",)