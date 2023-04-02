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
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import AsignarRolUsuarioForm
from .forms import ProyectoCreationForm

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
    
# CURD USUARIOS
# ----------------------------------------------------------
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
#------------------------------------------------------------

# CURD PROYECTOS
# ----------------------------------------------------------
class ProyectoCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoCreationForm
    template_name = 'proyecto_create.html'
    success_url = reverse_lazy('gestor:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = ProyectoCreationForm(self.request.POST)
            context['asignar_form'] = AsignarRolUsuarioForm(self.request.POST)
        else:
            context['form'] = ProyectoCreationForm()
            context['asignar_form'] = AsignarRolUsuarioForm()
        context['usuarios'] = User.objects.all()
        context['roles'] = Rol.objects.all()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        asignar_form = context['asignar_form']
        usuarios = asignar_form.cleaned_data.get('usuarios')
        rol = asignar_form.cleaned_data.get('rol')
        proyecto = form.save(commit=False)
        proyecto.usuario = self.request.user
        proyecto.save()
        for usuario in usuarios:
            for i in range(4):
                usu_proy_rol = UsuProyRol(usuario=usuario, rol=rol, proyecto=proyecto)
                usu_proy_rol.save()
        return super().form_valid(form)


class ProyectoUpdateView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    fields = ['nombre', 'descripcion']
    template_name = 'proyecto_update.html'
    success_url = reverse_lazy('gestor:proyecto_list')

class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    template_name = 'proyecto_delete.html'
    success_url = reverse_lazy('gestor:proyecto_list')

class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyecto_detail.html'
#------------------------------------------------------------


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
    
    def logout_view(request):
        logout(request)
        return redirect('login')