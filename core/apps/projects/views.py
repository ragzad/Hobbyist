from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm 
from django.contrib.auth.mixins import LoginRequiredMixin

# A view to display a list of all projects belonging to the logged-in user
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html' 
    context_object_name = 'projects'

    def get_queryset(self):
        # This ensures users only ever see their own projects
        return Project.objects.filter(owner=self.request.user)

# A view to display the details of a single project
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html' 
    context_object_name = 'project'

    def get_queryset(self):
        # This ensures a user can only see the detail page of their own project
        return Project.objects.filter(owner=self.request.user)
    
    # A view to create a new project
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html' 
    # Redirect to the project detail page after successful creation
    success_url = reverse_lazy('projects:project-list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.owner = self.request.user # Assign the logged-in user as the owner
        return super().form_valid(form)
    
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project-list')

    def get_queryset(self):
        # Ensure users can only update their own projects.
        return Project.objects.filter(owner=self.request.user)
    
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html' 
    success_url = reverse_lazy('projects:project-list')

    def get_queryset(self):
        # Ensure users can only delete their own projects.
        return Project.objects.filter(owner=self.request.user)