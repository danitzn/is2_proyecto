from django.urls import path
from .views import LoginView
from .views import DashboardView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
]