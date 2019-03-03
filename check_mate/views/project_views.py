from django.shortcuts import render
from check_mate.models import *

def projects(request):
    projects = Project.objects.all()
    context = {
        "projects": projects
    }
    return render(request, 'projects.html', context)