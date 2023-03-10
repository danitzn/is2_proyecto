from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from .models import Project
from .models import Task
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
        return '/dashboard'


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['proyectos'] = Project.objects.filter(usuario=self.request.user.id)
        context['tareas_pendientes'] = Task.objects.filter(usuario=self.request.user.id, estado='pendiente')
        context['tareas_en_proceso'] = Task.objects.filter(usuario=self.request.user.id, estado='en_proceso')
        context['tareas_terminadas'] = Task.objects.filter(usuario=self.request.user.id, estado='terminada')

        return context
