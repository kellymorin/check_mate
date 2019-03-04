from django.contrib.auth.models import User
from django.db import models

# Completed Models
# Project Board(id, name, description)
# user (first_name, last_name, email, password, username)
#  Ticket(id, project_id(foreign key), title, description)
# Tasks (id, ticket_id (foreign key), title, description)
# Ticket History(id, ticket_id(foreign key), user_id(foreign_key, mandatory), user_id(foreign_key, optional), activity_type(choices), timestamp)
# Task History(id, task_id(foreign key), user_id(foreign_key, mandatory), user_id(foreign_key, optional), activity_type(choices), timestamp)

# Create your models here.

class Project(models.Model):
    STATUS_TYPE_CHOICES=(
        ('Not Started', 'Not Started'),
        ('Active', 'Active'),
        ('Road Block', 'Road Block'),
        ('Complete', 'Complete')
    )
    project_name = models.CharField(max_length=100)
    project_description = models.TextField(blank=True, null=True)
    project_created = models.DateField(default=None, null=True, blank=True)
    project_due = models.DateField(default=None, null=True, blank=True)
    project_status = models.CharField(max_length=50, choices=STATUS_TYPE_CHOICES, default=None, blank=True, null=True )

    def __str__(self):
        return self.project_name


class Ticket(models.Model):
    STATUS_TYPE_CHOICES=(
        ('Not Started', 'Not Started'),
        ('Active', 'Active'),
        ('Ready for Review', 'Ready for Review'),
        ('Road Block', 'Road Block'),
        ('Complete', 'Complete')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ticket_name=models.CharField(max_length=100)
    ticket_description = models.TextField(blank=True, null=True)
    ticket_created = models.DateTimeField(default=None, null=True, blank=True)
    ticket_due = models.DateField(default=None, null=True, blank=True)
    ticket_status = models.CharField(max_length=50, choices=STATUS_TYPE_CHOICES, default=None, blank=True, null=True )

    def __str__(self):
        return self.ticket_name


class TicketHistory(models.Model):
    ACTIVITY_TYPE_CHOICES= (
        ('Comment', 'Comment'),
        ('Status', 'Status'),
        ('Assignment', 'Assignment')
    )
    STATUS_TYPE_CHOICES=(
        ('Not Started', 'Not Started'),
        ('Active', 'Active'),
        ('Ready for Review', 'Ready for Review'),
        ('Road Block', 'Road Block'),
        ('Complete', 'Complete')
    )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_active_user = models.ForeignKey(User, related_name="ticket_active_user", on_delete=models.CASCADE)
    ticket_affected_user = models.ForeignKey(User, related_name="ticket_affected_user", on_delete=models.CASCADE, default=None, null=True, blank=True),
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES, default=None)
    status = models.CharField(max_length=50, choices=STATUS_TYPE_CHOICES, default=None, blank=True, null=True )
    activity_description = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.ticket.ticket_name}:{self.activity_date} {self.activity_type}"


class Task(models.Model):
    STATUS_TYPE_CHOICES=(
        ('Not Started', 'Not Started'),
        ('Active', 'Active'),
        ('Ready for Review', 'Ready for Review'),
        ('Road Block', 'Road Block'),
        ('Complete', 'Complete')
    )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    task_name=models.CharField(max_length=100)
    task_description = models.TextField(blank=True, null=True)
    task_created = models.DateTimeField(default=None, null=True, blank=True)
    task_due = models.DateField(default=None, null=True, blank=True)
    task_status = models.CharField(max_length=50, choices=STATUS_TYPE_CHOICES, default=None, blank=True, null=True )

    def __str__(self):
        return self.task_name


class TaskHistory(models.Model):
    ACTIVITY_TYPE_CHOICES= (
        ('Comment', 'Comment'),
        ('Status', 'Status'),
        ('Assignment', 'Assignment')
    )
    STATUS_TYPE_CHOICES=(
        ('Not Started', 'Not Started'),
        ('Active', 'Active'),
        ('Ready for Review', 'Ready for Review'),
        ('Road Block', 'Road Block'),
        ('Complete', 'Complete')
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    task_active_user = models.ForeignKey(User, related_name="task_active_user",on_delete=models.CASCADE)
    task_affected_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_affected_user", default=None, null=True, blank=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES, default=None)
    status = models.CharField(max_length=50, choices=STATUS_TYPE_CHOICES, default=None, blank=True, null=True )
    activity_description = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.task.task_name}: {self.activity_date} {self.activity_type}"