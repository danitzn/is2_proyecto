from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.generic import FormView
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from .models import User
from .forms import UserForm

import logging

# Create your views here.
logger = logging.getLogger(__name__)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        # Authenticate the user
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('dashboard')
    

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    template_name = 'user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')


class UserUpdateView(UpdateView):
    model = User
    template_name = 'user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
