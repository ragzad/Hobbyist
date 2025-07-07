from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project

class ProjectCRUDTests(TestCase):

    def setUp(self):
        """
        This method runs before every single test function.
        We create two different users and a project for each one.
        """
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.project1 = Project.objects.create(
            owner=self.user1,
            name='User 1s Project',
            description='A test description.'
        )

        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.project2 = Project.objects.create(
            owner=self.user2,
            name='User 2s Project'
        )

    def test_project_model_str(self):
        """Test the __str__ method of the Project model."""
        self.assertEqual(str(self.project1), 'User 1s Project')

    def test_project_list_view_for_logged_in_user(self):
        """Test that a logged-in user can only see their own projects."""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('projects:project-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project1.name)
        self.assertNotContains(response, self.project2.name) # Crucial security check

    def test_project_list_view_for_logged_out_user(self):
        """Test that a logged-out user is redirected to the login page."""
        response = self.client.get(reverse('projects:project-list'))
        self.assertEqual(response.status_code, 302)
        # Check that the redirection is to the login page
        self.assertRedirects(response, '/accounts/login/?next=/projects/')

    def test_project_detail_view_security(self):
        """
        Test that a user can see their own project's detail page,
        but gets a 404 Not Found error for another user's project.
        """
        self.client.login(username='user1', password='password123')
        
        # User 1 tries to access their own project (should work)
        url_own = reverse('projects:project-detail', args=[self.project1.pk])
        response_own = self.client.get(url_own)
        self.assertEqual(response_own.status_code, 200)
        
        # User 1 tries to access User 2's project (should fail with 404)
        url_other = reverse('projects:project-detail', args=[self.project2.pk])
        response_other = self.client.get(url_other)
        self.assertEqual(response_other.status_code, 404)

    def test_project_create_view(self):
        """Test that a user can successfully create a new project."""
        self.client.login(username='user1', password='password123')
        url = reverse('projects:project-create')
        post_data = {'name': 'Newest Project', 'description': 'From a test.', 'status': 'IN_PROGRESS'}
        
        response = self.client.post(url, post_data)
        
        # Should redirect to the project list on success
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('projects:project-list'))
        
        # Verify the project was actually created in the database
        self.assertTrue(Project.objects.filter(name='Newest Project').exists())