from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')