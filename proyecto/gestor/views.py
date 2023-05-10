import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
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
from .forms import  SprintForm,UserStoryForm, UsuProyRolForm, UsuProyRolFormset, UsuarioCreationForm
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
from .forms import ProyectoForm
from django.shortcuts import get_object_or_404


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
    model = UserStory
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
class ProyectoCreateView(View):
    template_name = 'proyecto_create.html'

    def get(self, request):
        proyecto_form = ProyectoForm()
        usu_proy_rol_formset = UsuProyRolFormset()
        return render(request, self.template_name, {'proyecto_form': proyecto_form, 'usu_proy_rol_formset': usu_proy_rol_formset})

    def post(self, request):
        proyecto_form = ProyectoForm(request.POST)
        usu_proy_rol_formset = UsuProyRolFormset(request.POST)
        if proyecto_form.is_valid() and usu_proy_rol_formset.is_valid():
            proyecto = proyecto_form.save()
            for usu_proy_rol_form in usu_proy_rol_formset:
                usu_proy_rol = usu_proy_rol_form.save(commit=False)
                usu_proy_rol.proyecto = proyecto
                usu_proy_rol.save()
            return redirect('gestor:dashboard')
        else:
            return render(request, self.template_name, {'proyecto_form': proyecto_form, 'usu_proy_rol_formset': usu_proy_rol_formset})


class ProyectoUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_update.html'
    success_url = reverse_lazy('gestor:dashboard')


class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    template_name = 'proyecto_delete.html'
    success_url = reverse_lazy('gestor:proyecto_list')


class ProyectoDetailView(DetailView):
    model = Proyecto
    template_name = 'proyecto_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usu_proy_rol = UsuProyRol.objects.filter(proyecto=self.object)
        context['usu_proy_rol'] = usu_proy_rol
        return context


class UsuProyRolListView(View):
    model = UsuProyRol
    template_name = 'usu_proy_rol_list.html'

    def get(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        usu_proy_rol = UsuProyRol.objects.filter(proyecto=proyecto)
        return render(request, self.template_name, {'usu_proy_rol': usu_proy_rol, 'proyecto': proyecto})
    

class UsuProyRolUpdateView(UpdateView):
    model = UsuProyRol
    template_name = 'usu_proy_rol_update.html'
    fields = ['rol']

    def get_object(self, queryset=None):
        # Recuperar el objeto específico que se va a editar
        proyecto_pk = self.kwargs['pk']
        usu_pk = self.kwargs['usu_pk']
        obj = get_object_or_404(UsuProyRol, proyecto__pk=proyecto_pk, pk=usu_pk)
        # Aquí puedes aplicar cualquier lógica adicional para filtrar o modificar el objeto si es necesario
        return obj
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        pk = self.object.proyecto.pk
        success_url = reverse_lazy('gestor:proyecto_detail', kwargs={'pk': pk})
        self.object.save()

        return HttpResponseRedirect(success_url)
    

#------------------------------------------------------------

# CRUD SPRINTS
# ----------------------------------------------------------
class SprintCreateView(View):
    model = Sprint 
    template_name = 'sprint_create.html'

    def get(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        sprint_form = SprintForm(initial={'backlog':proyecto,'fecha_inicio': datetime.date.today(), 'fecha_fin': datetime.date.today() + datetime.timedelta(days=14), 'fecha_fin_prevista': datetime.date.today() + datetime.timedelta(days=14), 'duracion': 14})
        return render(request, self.template_name, {'sprint_form': sprint_form, 'proyecto': proyecto})

    def post(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        sprint_form = SprintForm(request.POST)
        if sprint_form.is_valid():
            sprint = sprint_form.save(commit=False)
            sprint.proyecto = proyecto
            sprint.save()
            return redirect('gestor:proyecto_detail', pk=pk)
        else:
            return render(request, self.template_name, {'sprint_form': sprint_form, 'proyecto': proyecto})
        

class SprintDetailView(DetailView):
    model = Sprint
    template_name = 'sprint_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user_stories = UserStory.objects.filter(sprint=self.object)
        # context['user_stories'] = user_stories
        proyecto = Proyecto.objects.get(pk=self.object.backlog.pk)
        context['proyecto'] = proyecto
        return context
    

class SprintUpdateView(UpdateView):
    model = Sprint
    template_name = 'sprint_update.html'
    fields = ['fecha_inicio', 'fecha_fin', 'fecha_fin_prevista']

    def get_object(self, queryset=None):
        # Recuperar el objeto específico que se va a editar
        proyecto_pk = self.kwargs['proyecto_pk']
        pk = self.kwargs['pk']
        obj = get_object_or_404(Sprint, backlog__pk=proyecto_pk, pk=pk)
        # Aquí puedes aplicar cualquier lógica adicional para filtrar o modificar el objeto si es necesario
        return obj
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        pk = self.object.proyecto.pk
        success_url = reverse_lazy('gestor:proyecto_detail', kwargs={'pk': pk})
        self.object.save()

        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = Proyecto.objects.get(pk=self.object.backlog.pk)
        context['proyecto'] = proyecto
        return context

        
#------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all projects
        proyectos = Proyecto.objects.all()
        sprints = []

        for proyecto in proyectos:
            sprint_pk = Sprint.objects.filter(backlog=proyecto.pk).order_by('-pk').first()
            sprints.append(sprint_pk)

        context['sprints'] = sprints
        context['proyectos'] = proyectos
        context['proyectos_sprints'] = zip(proyectos, sprints)

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
    

    #------------------------------------------------------------
    #user story
class UserStoryCreateView(View):
    template_name = 'user_story_create.html'
        
    def get(self, request):
        user_story_form = UserStoryForm()
        return render(request, self.template_name, {'user_story_form': user_story_form})
        
    def post(self, request):
        user_story_form = UserStoryForm(request.POST)
        if user_story_form.is_valid():
            user_story = user_story_form.save()
            return redirect('gestor:dashboard')
        else:
            return render(request, self.template_name, {'user_story_form': user_story_form})
            
        

class UserStoryListDetailView(View):
    model = UserStory
    template_name = 'user_story_detail.html'
    def get(self, request, pk):
        user_story = get_object_or_404(UserStory, pk=pk)
        return render(request, self.template_name, {'user_story': user_story})