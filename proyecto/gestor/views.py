from django.shortcuts import render
from .models import Proyecto
from .models import Sprint
from .models import Rol
from .models import UsuProyRol
from .models import Estados
from .models import UserStory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioCreationForm
from .forms import UsuarioChangeForm
from django.contrib.auth import login
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .forms import UsuarioCreationForm
from .forms import UsuarioChangeForm


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
        print('HOLAAAAAAAA')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('gestor:dashboard')
    

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UsuarioCreationForm
    template_name = 'usuario_create.html'
    success_url = reverse_lazy('gestor:usuario_list')


class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsuarioChangeForm
    template_name = 'usuario_update.html'
    success_url = reverse_lazy('gestor:usuario_list')


class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'usuario_delete.html'
    success_url = reverse_lazy('gestor:usuario_list')


class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'usuario_detail.html'

class UsuarioListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'usuario_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = User.objects.all()
        print('-------usuarios----------')
        print(User.objects.all())
        return context

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all projects
        proyectos = Proyecto.objects.all()
        context['proyectos'] = proyectos
        
        # Get all user stories
        user_stories = UserStory.objects.all()
        
        # Filter user stories by estado
        user_stories_hacer = user_stories.filter(estado__estado='hacer')
        user_stories_proceso = user_stories.filter(estado__estado='proceso')
        user_stories_terminado = user_stories.filter(estado__estado='terminado')
        
        context['user_stories_hacer'] = user_stories_hacer
        context['user_stories_proceso'] = user_stories_proceso
        context['user_stories_terminado'] = user_stories_terminado
        
        return context
    
    # def logout_view(request):
    #     logout(request)
    #     return redirect('login')