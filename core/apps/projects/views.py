from django.shortcuts import render, redirect, get_object_or_404 
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Project, InventoryItem, ProjectPhoto, Category, Task, Folder
from .forms import ProjectForm, PhotoUploadForm, InventoryItemForm, TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

# --- Homepage View ---
class HomeView(TemplateView):
    template_name = 'home.html'

# --- Project Views ---
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['folders'] = Folder.objects.filter(owner=user, folder_type='project')
        context['unfoldered_projects'] = Project.objects.filter(owner=user, folder__isnull=True)
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # Cost Calculation
        total_cost_data = project.required_inventory.aggregate(total=Sum('cost'))
        total_cost = total_cost_data.get('total') or 0
        context['total_project_cost'] = total_cost

        # Kanban & Form Context
        context['tasks_todo'] = project.tasks.filter(status='TODO')
        context['tasks_inprogress'] = project.tasks.filter(status='INPROGRESS')
        context['tasks_done'] = project.tasks.filter(status='DONE')
        context['task_form'] = TaskForm(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        if 'save_task' in request.POST:
            form = TaskForm(request.POST, request.FILES, user=request.user)
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
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['required_inventory'].queryset = InventoryItem.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        form.save_m2m() 
        messages.success(self.request, "Project created successfully!")
        return redirect('projects:project-list')

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['required_inventory'].queryset = InventoryItem.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, "Project updated successfully!")
        return super().form_valid(form)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['folders'] = Folder.objects.filter(owner=user, folder_type='inventory')
        context['unfoldered_items'] = InventoryItem.objects.filter(owner=user, folder__isnull=True)
        return context

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

# --- FOLDER & DRAG-DROP VIEWS ---
@require_POST
def create_folder(request):
    folder_name = request.POST.get('folder_name')
    folder_type = request.POST.get('folder_type', 'project')
    if folder_name:
        Folder.objects.create(name=folder_name, owner=request.user, folder_type=folder_type)
    if folder_type == 'inventory':
        return redirect('projects:inventory-list')
    return redirect('projects:project-list')

@require_POST
def move_project_to_folder(request):
    project_id = request.POST.get('project_id')
    folder_id = request.POST.get('folder_id')
    try:
        project = Project.objects.get(pk=project_id, owner=request.user)
        if folder_id == 'None':
            project.folder = None
        else:
            folder = Folder.objects.get(pk=folder_id, owner=request.user)
            project.folder = folder
        project.save()
        return HttpResponse(status=200)
    except (Project.DoesNotExist, Folder.DoesNotExist):
        return HttpResponse(status=404)

@require_POST
def move_inventory_item_to_folder(request):
    item_id = request.POST.get('item_id')
    folder_id = request.POST.get('folder_id')
    try:
        item = InventoryItem.objects.get(pk=item_id, owner=request.user)
        if folder_id == 'None':
            item.folder = None
        else:
            folder = Folder.objects.get(pk=folder_id, owner=request.user)
            item.folder = folder
        item.save()
        return HttpResponse(status=200)
    except (InventoryItem.DoesNotExist, Folder.DoesNotExist):
        return HttpResponse(status=404)

@require_POST
def move_task(request):
    task_id = request.POST.get('task_id')
    new_project_id = request.POST.get('new_project_id')

    print(f"DEBUG: move_task - task_id: {task_id}, new_project_id: {new_project_id}, user: {request.user.username}")

    if not task_id or not new_project_id:
        messages.error(request, "Missing task ID or new project ID for task move.")
        return redirect('projects:project-list')

    try:
        task = get_object_or_404(Task, pk=task_id, project__owner=request.user)
        new_project = get_object_or_404(Project, pk=new_project_id, owner=request.user)

        if task.project != new_project:
            task.project = new_project
            task.save() 
            messages.success(request, f"Task '{task.title}' moved successfully to project '{new_project.name}'.")
        else:
            messages.info(request, f"Task '{task.title}' is already in project '{new_project.name}'. No change made.")

        return redirect('projects:project-detail', pk=new_project_id)

    except Task.DoesNotExist:
        messages.error(request, "Task not found or you don't have permission to move it.")
        return redirect('projects:project-list')
    except Project.DoesNotExist:
        messages.error(request, "Target project not found or you don't have permission to move task to it.")
        return redirect('projects:project-list') 
    except Exception as e:
        messages.error(request, f"An unexpected error occurred while moving the task: {e}")
        import logging
        logger = logging.getLogger(__name__)
        logger.exception("Error in move_task view:")
        return redirect('projects:project-list') 