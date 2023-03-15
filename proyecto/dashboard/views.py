from django.shortcuts import render
from .models import Project
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


# Create your views here.
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
    
    # def logout_view(request):
    #     logout(request)
    #     return redirect('login')