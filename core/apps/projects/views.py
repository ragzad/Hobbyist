from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Project, InventoryItem, ProjectPhoto
from .forms import ProjectForm, PhotoUploadForm, InventoryItemForm
from django.contrib.auth.mixins import LoginRequiredMixin

# --- Homepage View ---
class HomeView(TemplateView):
    template_name = 'home.html'

# --- Project Views ---
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Project created successfully!")
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project-list')

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_premium = Profile.objects.filter(user=self.request.user, is_premium=True).exists()
        context['is_premium_user'] = is_premium
        if is_premium:
            context['photo_form'] = PhotoUploadForm()
        return context

    def post(self, request, *args, **kwargs):
        is_premium = Profile.objects.filter(user=self.request.user, is_premium=True).exists()
        if not is_premium:
            return redirect('projects:project-list')

        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.project = self.get_object()
            photo.save()
        return redirect('projects:project-detail', pk=self.get_object().pk)

# --- INVENTORY VIEWS ---
class InventoryListView(LoginRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

class InventoryItemCreateView(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('projects:inventory-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Inventory item added successfully!")
        return super().form_valid(form)

class InventoryItemUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('projects:inventory-list')

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

class InventoryItemDeleteView(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('projects:inventory-list')

    def get_queryset(self):
        return