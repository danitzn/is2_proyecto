from django.urls import path
from .views import DashboardView
from .views import LoginView
from .views import (
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView,
    UsuarioDetailView,
    UsuarioListView,
)
from .views import (
    ProyectoCreateView,
    ProyectoUpdateView,
    ProyectoDeleteView,
    ProyectoDetailView,
)

app_name = 'gestor'


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('gestor/usuarios/nuevo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('gestor/usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('gestor/usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuario_delete'),
    path('gestor/usuarios/<int:pk>/', UsuarioDetailView.as_view(), name='usuario_detail'),
    path('gestor/usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('gestor/proyectos/nuevo/', ProyectoCreateView.as_view(), name='proyecto_create'),
    path('gestor/proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('gestor/proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto_delete'),
    path('gestor/proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto_detail'),
]