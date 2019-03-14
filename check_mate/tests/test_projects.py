import unittest
import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import Project, Ticket


class ProjectTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectTest, cls).setUpClass()

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
            project_status = "Not Started"
        )

        # Create project
        project2 = Project.objects.create(
            project_name = "Project 2",
            project_description = "This is a second test project for the testing suite to use.",
            project_created = today,
            project_status = "Active"
        )

        # Create ticket 1 for project 2
        ticket = Ticket.objects.create(
            ticket_name = "Ticket",
            ticket_description = "This is a test ticket for the testing suite to use",
            project = project2,
            ticket_status = "Not Started",
            ticket_assigned_user = new_user,
            ticket_created = today
        )

        # Create ticket 2 for project 2
        ticket2 = Ticket.objects.create(
            ticket_name = "Ticket",
            ticket_description = "This is a second test ticket for the testing suite to use",
            project = project2,
            ticket_status = "Active",
            ticket_assigned_user = new_user,
            ticket_created = today
        )

        # Create ticket 3 for project 2
        ticket3 = Ticket.objects.create(
            ticket_name = "Ticket",
            ticket_description = "This is a third test ticket for the testing suite to use",
            project = project2,
            ticket_status = "Complete",
            ticket_assigned_user = new_user,
            ticket_created = today
        )

    def test_list_projects(self):
        """Test case verifies that the projects are listed when the navbars 'projects' link is clicked"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse('check_mate:projects'))

        # Check that when the user is logged out, they are redirected to login page
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a new GET request
        response = self.client.get(reverse('check_mate:projects'))

        # Check that the response is 200
        self.assertEqual(response.status_code, 200)

        # Check that the context contains 2 products
        self.assertEqual(len(response.context['projects']), 2)

        # TODO: add check for response content once final styling and formatting is finalized

    def test_get_project_detail(self):
        """Test case verifies that a specific project details are rendered when a specific project is selected from the project list"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse('check_mate:project_details', args=(1,)))

        # Check that when the user is logged out, they are redirected to the login page
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a new GET request
        response = self.client.get(reverse('check_mate:project_details', args=(1,)))

        # Check that the response is 200
        self.assertEqual(response.status_code, 200)

        # Check that the project detail page does not display any tickets
        self.assertEqual(len(response.context['tickets']), 0)

        # Issue a new GET request for a project with associated tickets
        other_project = self.client.get(reverse('check_mate:project_details', args=(2,)))

        # Check that the response is 200
        self.assertEqual(other_project.status_code, 200)

        # Check the the context contains 3 tickets
        self.assertEqual(len(other_project.context['tickets']), 3)

        # TODO: Add check for response content once final styling and formatting is finalized

    def test_edit_project_form(self):
        """Test case verifies that the project edit form loads with expected fields if the user is authenticated"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:project_edit", args=(1,)))

        # Confirm that there is no content in the response
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they are not authenticated
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue another GET request
        response = self.client.get(reverse("check_mate:project_edit", args=(1,)))

        # Confirm that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Confirm that the response does have associated content
        self.assertTrue(response.content)

        # TODO: Write test for response content once final styling and formatting is added

    def test_project_delete(self):
        """Tests that an authenticated user can delete a project if certain conditions are met"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:project_delete", args=(1, )))

        # Confirm that the response does not have content
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they have not been logged in
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a GET request for a project that cannot be deleted
        get_delete = self.client.get(reverse("check_mate:project_delete", args=(2,)))

        # Confirm that the response is 200
        self.assertEqual(get_delete.status_code, 200)

        # Confirm that the context has "can delete" set to False
        self.assertEqual(get_delete.context["project"].delete_status, False)

        # Issue another GET request for a project that can be deleted
        get_delete_true = self.client.get(reverse("check_mate:project_delete", args=(1,)))

        # Confirm that the response is 200
        self.assertEqual(get_delete_true.status_code, 200)

        # Confirm that the context has "can delete" set to True
        self.assertEqual(get_delete_true.context["project"].delete_status, True)

        # TODO: Write tests for content that displays on the page
        # TODO: Write tests for post functionality of delete


    # def test_edit_project_detail(self):
        # """Test case verifies that you can edit a specific project and the request successfully saves"""

        # TODO: Write testing suite for edit


    def test_add_project_form(self):
        """Test case verifies that the project add form page loads with expected fields if user is authenticated"""

        # Issue a GET request
        logged_out_response = self.client.get(reverse("check_mate:project_add"))

        # Confirm that the response does not have any content
        self.assertFalse(logged_out_response.content)

        # Confirm that the user is redirected to the login page if they are not authenticated
        self.assertEqual(logged_out_response.status_code, 302)

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a GET request
        response = self.client.get(reverse("check_mate:project_add"))

        # Confirm that the response is 200
        self.assertEqual(response.status_code, 200)

        # TODO: Write check for response content once final styling and formatting is added

    def test_add_project(self):
        """Test case verifies that you can add a new project and it successfully saves"""

        # Log the user in
        self.client.login(username="test_user", password="secret")

        # Issue a POST request with a new project
        response = self.client.post(reverse("check_mate:project_add"), {"project_name": "New Project", "project_description": "This is a new project.", "project_due": "2019-05-02"})

        # Confirm that the response redirects to the all projects page
        self.assertEqual(response.status_code, 302)

        # TODO: Add test for submitting incorect or incomplete data

        # TODO: Check the content on the all projects page to ensure that the new project is listed



