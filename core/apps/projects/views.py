from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, ProjectPhoto
from .forms import ProjectForm, PhotoUploadForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# --- Project List View ---
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

    def get_context_data(self, **kwargs):
        # This method lets us add extra context to the template
        context = super().get_context_data(**kwargs)
        # Check if the user's profile exists and is premium
        is_premium = hasattr(self.request.user, 'profile') and self.request.user.profile.is_premium
        context['is_premium_user'] = is_premium
        return context
    
    # A view to create a new project
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Project created successfully!") # Add this message
        return super().form_valid(form)

# --- Project Update View ---
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project-list')

    def get_queryset(self):
        # Ensure users can only update their own projects.
        return Project.objects.filter(owner=self.request.user)

# --- Project Delete View ---
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project-list')

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

# --- Project Detail View (with Photo Upload) ---
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_premium = hasattr(self.request.user, 'profile') and self.request.user.profile.is_premium
        context['is_premium_user'] = is_premium
        if is_premium:
            context['photo_form'] = PhotoUploadForm()
        return context

    def post(self, request, *args, **kwargs):
        # This is the crucial method that handles POST requests for this view.
        # Without it, you get a 405 error.
        is_premium = hasattr(self.request.user, 'profile') and self.request.user.profile.is_premium
        if not is_premium:
            return redirect('projects:project-list')

        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.project = self.get_object()
            photo.save()
            
        return redirect('projects:project-detail', pk=self.get_object().pk)