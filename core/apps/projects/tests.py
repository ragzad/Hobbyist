from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Project, Task, InventoryItem
from .forms import ProjectForm


class ProjectModelTest(TestCase):
    """
    Tests for the Project, Task, and InventoryItem models.
    """

    def setUp(self):
        """Set up test users and data."""
        self.user1 = User.objects.create_user(
            username='user1', password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='password123'
        )
        self.project = Project.objects.create(user=self.user1, title='Test Project 1')
        self.item1 = InventoryItem.objects.create(
            user=self.user1, name='Wood', cost=10.50
        )
        self.item2 = InventoryItem.objects.create(
            user=self.user1, name='Screws', cost=5.00
        )
        self.project.inventory.add(self.item1, self.item2)

    def test_project_creation(self):
        """Test that a project is created correctly."""
        self.assertEqual(self.project.title, 'Test Project 1')
        self.assertEqual(self.project.user, self.user1)

    def test_get_total_cost(self):
        """Test the project's total cost calculation method."""
        self.assertEqual(self.project.get_total_cost(), 15.50)

    def test_task_ordering(self):
        """Test that tasks are ordered correctly."""
        Task.objects.create(project=self.project, title='Task 2', order=1)
        Task.objects.create(project=self.project, title='Task 1', order=0)
        tasks = self.project.tasks.all()
        self.assertEqual(tasks[0].title, 'Task 1')
        self.assertEqual(tasks[1].title, 'Task 2')


class ProjectViewsTest(TestCase):
    """
    Tests for the views in the 'projects' app.
    """
    def setUp(self):
        """Set up test users, data, and a logged-in client."""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        self.project = Project.objects.create(user=self.user, title='My Test Project')
        self.other_project = Project.objects.create(
            user=self.other_user, title="Other User's Project"
        )

    def test_project_list_view(self):
        """Test that the project list shows only the user's projects."""
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_list.html')
        self.assertContains(response, self.project.title)
        self.assertNotContains(response, self.other_project.title)

    def test_project_detail_view_permissions(self):
        """Test that a user can only view their own project details."""
        # Test access to own project
        response_own = self.client.get(reverse('project-detail', args=[self.project.pk]))
        self.assertEqual(response_own.status_code, 200)
        self.assertContains(response_own, self.project.title)

        # Test access to other's project (should fail test_func -> 403 Forbidden)
        response_other = self.client.get(reverse('project-detail', args=[self.other_project.pk]))
        self.assertEqual(response_other.status_code, 403)

    def test_project_create_view(self):
        """Test the creation of a new project."""
        response = self.client.post(reverse('project-create'), {
            'title': 'New Created Project',
            'description': 'A description.'
        })
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertTrue(Project.objects.filter(title='New Created Project').exists())
        new_project = Project.objects.get(title='New Created Project')
        self.assertEqual(new_project.user, self.user)

    def test_project_update_view_permissions(self):
        """Test that a user can only update their own projects."""
        response = self.client.post(reverse('project-update', args=[self.project.pk]), {
            'title': 'Updated Title',
            'description': self.project.description
        })
        self.assertEqual(response.status_code, 302) # Redirect
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Title')

        # Try to update other user's project
        response_other = self.client.post(reverse('project-update', args=[self.other_project.pk]), {
            'title': 'Malicious Update'
        })
        self.assertEqual(response_other.status_code, 403) # Forbidden

    def test_project_delete_view(self):
        """Test the deletion of a project."""
        response = self.client.post(reverse('project-delete', args=[self.project.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())


class TaskHtmxViewsTest(TestCase):
    """
    Tests for the HTMX-based task views.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='htmxuser', password='password')
        self.client = Client()
        self.client.login(username='htmxuser', password='password')
        self.project = Project.objects.create(user=self.user, title='HTMX Project')

    def test_add_task(self):
        """Test adding a task via HTMX."""
        url = reverse('add-task', args=[self.project.pk])
        response = self.client.post(url, {'title': 'New HTMX Task'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(title='New HTMX Task').exists())
        self.assertTemplateUsed(response, 'tasks/partials/task_item.html')

    def test_delete_task(self):
        """Test deleting a task via HTMX."""
        task = Task.objects.create(project=self.project, title='Task to delete')
        url = reverse('delete-task', args=[task.pk])
        # Note: HTMX delete requests are sent as DELETE method
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())