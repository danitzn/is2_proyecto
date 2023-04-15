from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Proyecto
from .models import Rol
from .models import UsuProyRol
from django.forms import modelform_factory
from django.forms import formset_factory


# FORMS USUARIOS
# ----------------------------------------------------------
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')
# ----------------------------------------------------------

# FORMS PROYECTOS
# ----------------------------------------------------------
ProyectoForm = modelform_factory(Proyecto, fields=('nombre', 'descripcion'))

class UsuProyRolForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())

    class Meta:
        model = UsuProyRol
        fields = ('usuario', 'rol')

UsuProyRolFormset = formset_factory(UsuProyRolForm, extra=4)

# ----------------------------------------------------------