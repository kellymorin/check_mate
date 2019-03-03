from django.urls import path
from . import views

app_name = "check_mate"

urlpatterns=[
    path("", views.index, name='index')
]