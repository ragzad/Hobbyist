from django.views.generic import ListView, DetailView
from .models import Project
from django.contrib.auth.mixins import LoginRequiredMixin

# A view to display a list of all projects belonging to the logged-in user
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html' # We will create this file next
    context_object_name = 'projects'

    def get_queryset(self):
        # This ensures users only ever see their own projects
        return Project.objects.filter(owner=self.request.user)

# A view to display the details of a single project
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html' # We will create this file next
    context_object_name = 'project'

    def get_queryset(self):
        # This ensures a user can only see the detail page of their own project
        return Project.objects.filter(owner=self.request.user)