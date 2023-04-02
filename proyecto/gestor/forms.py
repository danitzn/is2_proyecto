from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Proyecto
from .models import Rol


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
class ProyectoCreationForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProyectoUpdateForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
# ----------------------------------------------------------

class AsignarRolUsuarioForm(forms.Form):
    usuarios = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all())
