import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from check_mate.models import *



# @login_required
# def task_add(request):
# When the user selects the option to add a new related task
# Then they should be presented with a form, where they can provide information about the task such as name, description, status and assigned team member

# When the user submits the form
# If the data is valid, they will be taken back to the ticket detail page with the related task added
# If the data is not valid, they will be shown an error message on the form and asked to supply valid data


# @login_required
# def task_edit(request, task_id):
# When the user selects the option to edit task details
# Then they should be presented with a form, that is pre-populated with existing task data, where they can update information about the task such as name, description, status and assigned team member

# When the user submits the form
# If the data is valid, they will be taken back to the ticket detail page with the related task updated completed
# If the data is not valid, they will be shown an error message on the form and asked to supply valid data

# @login_required
# def task_delete(request, task_id):
# And an option to delete the entire task

# When the user selects the options to delete
# Then they will be presented with an option to confirm that they would like to delete the task

# If the user confirms deletion
# Then they will be taken back to the ticket detail page, with the related task removed from the list

# If the user cancels deletion
# Then they will be taken back to the ticket detail page, with no changes made to the related task
