from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    """Defines a current, upcoming or past project


    Returns:
        __str__ -- Project name
    """

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

    @property
    def get_ticket_status(self):
        all_tickets = Ticket.objects.filter(project = self.id)

        ticket_status={"Not Started": 0, "Active": 0, "Ready for Review": 0, "Road Block": 0, "Complete": 0, "Total": len(all_tickets)}
        for ticket in all_tickets:
            ticket_status[ticket.ticket_status] += 1

        return ticket_status

    def __str__(self):
        return self.project_name


class Ticket(models.Model):
    """Defines a ticket and associates it with a project instance


    Returns:
        __str__ -- Ticket Name
    """

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
    ticket_assigned_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, default=None)

    @property
    def get_task_status(self):
        all_tasks = Task.objects.filter(ticket = self.id)

        task_status={"Not Started": 0, "Active": 0, "Ready for Review": 0, "Road Block": 0, "Complete": 0, "Total": len(all_tasks)}
        for task in all_tasks:
            task_status[task.task_status] += 1

        return task_status

    def __str__(self):
        return self.ticket_name


class TicketHistory(models.Model):
    """Captures all activity on a ticket: including changes to status, assignments and comments

    Returns:
        __str__ -- Ticket Name, Activity Date and Activity Type
    """

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
    ticket_affected_user = models.ForeignKey(User, related_name="ticket_affected_user", on_delete=models.CASCADE, default=None, null=True, blank=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES, default=None)
    status = models.CharField(max_length=50, choices=STATUS_TYPE_CHOICES, default=None, blank=True, null=True )
    activity_description = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.ticket.ticket_name}:{self.activity_date} {self.activity_type}"


class Task(models.Model):
    """Defines a task and associates it with a ticket instance


    Returns:
        __str__ -- Task Name
    """

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
    task_assigned_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, default=None, blank=True)

    def __str__(self):
        return self.task_name


class TaskHistory(models.Model):
    """Captures all activity on a task: including changes to status, assignments and comments

    Returns:
        __str__ -- Task Name, Activity Date and Activity Type
    """
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