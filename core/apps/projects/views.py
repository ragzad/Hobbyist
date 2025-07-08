from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Project, InventoryItem, ProjectPhoto, Category, Task
from .forms import ProjectForm, PhotoUploadForm, InventoryItemForm, TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.decorators.http import require_POST

# --- Homepage View ---
class HomeView(TemplateView):
    template_name = 'home.html'

# --- Project Views ---
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['tasks_todo'] = project.tasks.filter(status='TODO')
        context['tasks_inprogress'] = project.tasks.filter(status='INPROGRESS')
        context['tasks_done'] = project.tasks.filter(status='DONE')
        context['task_form'] = TaskForm()
        total_cost_data = project.required_inventory.aggregate(total=Sum('cost'))
        total_cost = total_cost_data.get('total') or 0
        context['total_project_cost'] = total_cost
        is_premium = Profile.objects.filter(user=self.request.user, is_premium=True).exists()
        context['is_premium_user'] = is_premium
        if is_premium:
            context['photo_form'] = PhotoUploadForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = self.get_object()
            task.save()
            messages.success(request, "New task added to 'To Do'.")
        else:
            messages.error(request, "There was an error adding your task.")
        return redirect('projects:project-detail', pk=self.get_object().pk)

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Inventory item added successfully!")
        return super().form_valid(form)

class InventoryItemUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('projects:inventory-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class InventoryItemDeleteView(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('projects:inventory-list')

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

# --- TASK VIEWS ---
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.object.project.pk})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.object.project.pk})
    
@require_POST
def move_task(request):
    # This view is called by htmx when a task is moved
    task_id = request.POST.get('task_id')
    new_status = request.POST.get('new_status')
    
    try:
        task = Task.objects.get(pk=task_id, project__owner=request.user)
        task.status = new_status
        task.save()
        return HttpResponse(status=200) # Success
    except Task.DoesNotExist:
        return HttpResponse(status=404) # Not Found
    except Exception as e:
        return HttpResponse(status=500) # Server Error