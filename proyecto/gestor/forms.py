from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Estados, Proyecto, Sprint, UserStory
from .models import Rol
from .models import UsuProyRol
from django.forms import modelform_factory
from django.forms import formset_factory
from django.forms.widgets import DateInput


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

UsuProyRolFormset = formset_factory(UsuProyRolForm, extra=3)

# ----------------------------------------------------------
# FORMS USER STORY
# ----------------------------------------------------------
class UserStoryForm(forms.ModelForm):
    sprint = forms.ModelChoiceField(queryset=Sprint.objects.all())
    estado = forms.ModelChoiceField(queryset=Estados.objects.all())
    usu_proy_rol = forms.ModelChoiceField(queryset=UsuProyRol.objects.all())
    class Meta:
        model = UserStory
        fields = ('nombre', 'descripcion','usu_proy_rol','sprint','estado')
        UserStoryFormset = formset_factory(UserStory, extra=4)


class SprintForm(forms.ModelForm):
    backlog = forms.ModelChoiceField(queryset=Proyecto.objects.all())
    fecha_inicio = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    fecha_fin_prevista = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    duracion = forms.IntegerField()

    class Meta:
        model = Sprint
        fields = ('backlog', 'fecha_inicio', 'fecha_fin', 'fecha_fin_prevista', 'duracion')

class SprintUpdateForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    fecha_fin_prevista = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    duracion = forms.IntegerField()

    class Meta:
        model = Sprint
        fields = ('fecha_inicio', 'fecha_fin', 'fecha_fin_prevista', 'duracion')
