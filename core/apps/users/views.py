from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView 
from django.contrib.auth.mixins import LoginRequiredMixin 
from .forms import SignUpForm, UserUpdateForm

class SignUpView(CreateView):
    form_class = SignUpForm
    # Redirect to the login page after successful registration
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('projects:project-list') # Redirect to dashboard on success

    def get_object(self):
        # This method ensures the form is always for the currently logged-in user
        return self.request.user