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

app_name = 'gestor'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('gestor/nuevo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('gestor/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('gestor/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuario_delete'),
    path('gestor/<int:pk>/', UsuarioDetailView.as_view(), name='usuario_detail'),
    path('gestor/', UsuarioListView.as_view(), name='usuario_list'),
]