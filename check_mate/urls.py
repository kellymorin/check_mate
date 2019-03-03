from django.urls import path
from . import views

app_name = "check_mate"

urlpatterns=[
    path("", views.index, name='index'),
    # ex. /login
    path("login", views.login_user, name="login"),
    # ex. /logout
    path("logout", views.user_logout, name="logout"),
    # ex. /register
    path("register", views.register, name="register")
]