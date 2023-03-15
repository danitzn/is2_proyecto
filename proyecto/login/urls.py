from django.urls import path
from .views import LoginView
from .views import UserListView
from .views import UserCreateView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('listUser', UserListView.as_view(), name='listUser'),
    path('createUser', UserCreateView.as_view(), name='createUser'),
]