from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project

class ProjectModelAndViewsTest(TestCase):

    def setUp(self):
        # This method runs before every test function.
        # We create a user and a project that our tests can use.
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project = Project.objects.create(
            owner=self.user,
            name='Test Project',
            description='A test description.'
        )

    def test_project_model_str(self):
        """
        Test the __str__ method of the Project model.
        """
        self.assertEqual(str(self.project), 'Test Project')

    def test_project_list_view_for_logged_in_user(self):
        """
        Test that the project list view works for a logged-in user.
        """
        # Log the user in
        self.client.login(username='testuser', password='password123')
        
        # Get the URL for the project list
        url = reverse('projects:project-list')
        response = self.client.get(url)

        # Check that the response is successful (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'projects/project_list.html')

    def test_project_list_view_for_logged_out_user(self):
        """
        Test that the project list view redirects a logged-out user.
        """
        # Get the URL for the project list
        url = reverse('projects:project-list')
        response = self.client.get(url)

        # Check that the user is redirected (HTTP 302)
        self.assertEqual(response.status_code, 302)
        # Check that the redirection is to the login page
        self.assertRedirects(response, '/accounts/login/?next=/projects/')