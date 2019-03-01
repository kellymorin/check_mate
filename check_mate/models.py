from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# Tasks (id, ticket_id (foreign key), title, description)
#  Ticket(id, project_id(foreign key), title, description)
# Project Board(id, name, description)
# user (first_name, last_name, email, password, username)
# Ticket History(id, ticket_id(foreign key), user_id(foreign_key, mandatory), user_id(foreign_key, optional), activity_type(choices), timestamp)
# Task History(id, task_id(foreign key), user_id(foreign_key, mandatory), user_id(foreign_key, optional), activity_type(choices), timestamp)