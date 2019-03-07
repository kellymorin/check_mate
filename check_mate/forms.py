from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django import forms

from check_mate.models import *


class LogInForm(forms.ModelForm):
    """Handles log in and authentication of existing users"""

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=("username", "password")


class UserForm(forms.ModelForm):
    """Handles registration of new users"""

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")


class ProjectForm(forms.ModelForm):
    """Handles displaying the add/edit form for projects"""

    class Meta:
        model = Project
        fields = ("project_name", "project_description", "project_due")
        widgets = {
            "project_due": forms.DateInput(attrs={"type": "date"})
        }


class TicketForm(forms.ModelForm):
    """Handles displaying the add/edit form for tickets"""

    class Meta:
        model = Ticket
        fields = ("ticket_name", "ticket_description", "ticket_due", "ticket_assigned_user")
        widgets = {
            "ticket_due": forms.DateInput(attrs={"type": "date"})
        }


class TicketStatusForm(forms.ModelForm):
    """Handles displaying the ticket status for status updates during the edit process"""

    class Meta:
        model = Ticket
        fields = ("ticket_status",)


class TaskForm(forms.ModelForm):
    """Handles displaying the add/edit form for tasks"""

    class Meta:
        model = Task
        fields = ("task_name", "task_description", "task_due", "task_assigned_user")
        widgets = {
            "task_due": forms.DateInput(attrs={"type": "date"})
        }


class TaskStatusForm(forms.ModelForm):
    """Handles displaying the task status for status updates during the edit process"""

    class Meta:
        model = Task
        fields = ("task_status",)