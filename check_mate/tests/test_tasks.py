import unittest
import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import *

class TaskTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TaskTest, cls).setUpClass()

        today = datetime.date.today()

        #Create User
        new_user = User.objects.create_user(
            username="test_user",
            first_name="Test",
            last_name = "User",
            email = "test@test.com",
            password="secret"
        )

        # Create project
        project = Project.objects.create(
            project_name = "Project",
            project_description = "This is a test project for the testing suite to use.",
            project_created = today,
            project_status = "Active"
        )

        # Create ticket 1 for project
        ticket = Ticket.objects.create(
            ticket_name = "Ticket",
            ticket_description = "This is a test ticket for the testing suite to use",
            project = project,
            ticket_status = "Not Started",
            ticket_assigned_user = new_user,
            ticket_created = today
        )

        # Create task 1 for ticket
        task = Task.objects.create(
            task_name = "Task",
            task_description = "This is a test task for the tesing suite to use",
            ticket = ticket,
            task_status = "Not Started",
            task_created = today,
            task_assigned_user = new_user,
        )

        # Create task 2 for ticket
        task2 = Task.objects.create(
            task_name = "Task 2",
            task_description = "This is a second test task for the testing suite to use",
            ticket = ticket,
            task_status = "Active",
            task_created = today,
            task_assigned_user = new_user,
        )

    def test_add_task_form(self):
        """Test case verifies that the task add form page loads with expected fields if the user is authenticated"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:task_add"))

        # Confirm that the response does not have any content
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they are not authenticated
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # TODO: Figure out how to pass ticket information in the form
        # TODO: Write check for response content once final styling and formatting is added

    def test_add_task(self):
        """Test case verifies that you can add a new task and it successfully saves"""

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a POST request with a new task
        response = self.client.post(reverse("check_mate:task_add"), {"task_name": "New Task", "task_description": "Test task", "task_status": "Not Started", "task_due": "2019-05-02", "ticket": "1", "task_assigned_user": "1"})

        # Confirm that the response redirects to the ticket detail page
        self.assertEqual(response.status_code, 302)

        # TODO: Add test for submitting incorrect or incomplete data

        # TODO: Check content on ticket detail page to ensure that new task is listed

    def test_edit_task_form(self):
        """Test case verifies that the task edit form pagee loads with expected fields if the user is authenticated"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:task_edit", args=(1,)))

        # Confirm that the response does not have associated content
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they are not authenticated
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a GET request
        response = self.client.get(reverse("check_mate:task_edit", args=(1,)))

        # Confirm that the response is 200
        self.assertEqual(response.status_code, 200)

        # TODO: Write check for the response content once final styling and formatting is added


    # def test_edit_task(self):
        # """Test case verifies that you can edit a specific task and the request successfully saves"""

        # TODO: Write testing suite for edit task

    def test_delete_task(self):
        """Test case verifies that you can delete a task if the user is authenticated and certain conditions are met"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:task_delete", args=(1,)))

        # Confirm that the response does not have any content
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they are not authenticated
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a GET request for a task that cannot be deleted
        get_delete = self.client.get(reverse("check_mate:task_delete", args=(2,)))

        # Confirm that the response is 200
        self.assertEqual(get_delete.status_code, 200)

        # Confirm that the context has "can delete" set to False
        self.assertEqual(get_delete.context["can_delete"], False)

        # Issue another GET request for a task that can be deleted
        get_delete_true = self.client.get(reverse("check_mate:task_delete", args=(1,)))

        # Confirm that the response is 200
        self.assertEqual(get_delete_true.status_code, 200)

        # Confirm that the context has "can_delete" set to True
        self.assertEqual(get_delete_true.context["can_delete"], True)

        # TODO: Write tests for content that displays on the page
        # TODO: Writee tests for post functionality of delete



