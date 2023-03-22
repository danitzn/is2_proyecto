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

app_name = 'usuarios'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('usuarios/nuevo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuario_delete'),
    path('usuarios/<int:pk>/', UsuarioDetailView.as_view(), name='usuario_detail'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
]