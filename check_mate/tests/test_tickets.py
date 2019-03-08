import unittest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import *

class TicketTest(TestCase):

    @classmethod
    def setUpClass(cls):

        super(TicketTest, cls).setUpClass()

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

        # Create project
        project2 = Project.objects.create(
            project_name = "Project 2",
            project_description = "This is a second test project for the testing suite to use.",
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

        # Create ticket for project 2
        ticket2 = Ticket.objects.create(
            ticket_name = "Ticket",
            ticket_description = "This is a second test ticket for the testing suite to use",
            project = project2,
            ticket_status = "Active",
            ticket_assigned_user = new_user,
            ticket_created = today
        )

        # Create task 1 for ticket
        task = Task.objects.create(
            task_name = "Task",
            task_description = "This is a test task for the tesing suite to use",
            ticket = ticket,
            task_status = "Active",
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

        # Create task 3 for ticket
        task3 = Task.objects.create(
            task_name = "Task",
            task_description = "This is a test task for the tesing suite to use",
            ticket = ticket,
            task_status = "Complete",
            task_created = today,
            task_assigned_user = new_user,
        )


    def test_ticket_detail(self):
        """Test case verified that a specific ticket details are rendered when a specific ticket is selected from the project board"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse('check_mate:ticket_details', args=(1,)))

        # Confirm that if the user is logged out they are redirected to the login page
        self.assertEqual(logged_out_response.status_code, 302)

        # Log User In
        self.client.login(username="test_user", password="secret")

        # Issue another GET request
        response = self.client.get(reverse("check_mate:ticket_details", args=(1,)))

        # Confirm that the response is 200
        self.assertEqual(response.status_code, 200)

        # Confirm that the ticket detail has 3 associated tasks
        self.assertEqual(len(response.context['tasks']), 3)

        # Issue GET request for tickets with no tasks
        other_ticket = self.client.get(reverse('check_mate:ticket_details', args=(2,)))

        # Confirm that the response is 200
        self.assertEqual(other_ticket.status_code, 200)

        # Confirm that the ticket detail has no associated tasks
        self.assertEqual(len(other_ticket.context['tasks']), 0)

        # TODO: Add check for response content once final styling and formatting is finalized

    def test_edit_ticket_form(self):
        """Test case verifies that the ticket edit form loads with expected fields if the user is authenticated"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:ticket_edit", args=(1,)))

        # Confirm that there is no content in the reesponse
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they are not authenticated
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a GET request
        response = self.client.get(reverse("check_mate:ticket_edit", args=(1,)))

        # Confirm that the response is 200
        self.assertEqual(response.status_code, 200)

        # TODO: Write check for response content once final styling and formatting is added


    # def test_edit_ticket(self):
        # """Test case verifies that you can edit a specific ticket and the request successfully saves"""
        # TODO: Write testing suite for edit functionality

    def test_add_ticket_form(self):
        """Test case verifies that the ticket add form loads with expected fields if the user is authenticated"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:ticket_add"))

        # Confirm that the response does not have any content
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they are not authenticated
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # TODO: Figure out how to pass in project information for the form

        # response = self.client.get(reverse("check_mate:ticket_add", args=(1,)))

        # self.assertEqual(response.status_code, 200)

        # TODO: Write check for response content once final styling and formatting is added

    def test_add_ticket(self):
        """Test case verifies that an authenticated user can successfully create a ticket"""

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a POST request with a new project
        response = self.client.post(reverse("check_mate:ticket_add"), {"ticket_name": "New Ticket", "ticket_description": "Test ticket", "ticket_status": "Active", "ticket_due": "2019-05-02", "project": "1", "ticket_assigned_user": "1"})

        # Confirm that the response redirects to project detail page
        self.assertEqual(response.status_code, 302)

        # TODO: Add test for submitting incorect or incomplete data

        # TODO: Check the content on project detail page to ensure that the new ticket is listed

    def test_ticket_delete(self):
        """Tests that an authenticated user can delete a ticket if certain conditions are met"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:ticket_delete", args=(1,)))

        # Confirm that the response does not have any content
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they are not authenticated
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a GET request for a ticket that cannot be deleted
        get_delete = self.client.get(reverse("check_mate:ticket_delete", args=(1,)))

        # Confirm that the response is 200
        self.assertEqual(get_delete.status_code, 200)

        # Confirm that the context has "can delete" set to False
        self.assertEqual(get_delete.context['can_delete'], False)

        # Issue another GET request for a ticket that can be deleted
        get_delete_true = self.client.get(reverse("check_mate:ticket_delete", args=(2,)))

        # Confirm that the response is 200
        self.assertEqual(get_delete_true.status_code, 200)

        # Confirm that the context has "can delete" set to True
        self.assertEqual(get_delete_true.context["can_delete"], True)

        # TODO: Write tests for content that displays on the page
        # TODO: Write tests for post functionality of delete


        # response = self.client.post(reverse("website:delete_product", args=(1,)))

        # self.assertEqual(response.status_code, 302)




