from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os


# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre
    
    
class Sprint(models.Model):
    backlog = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_fin_prevista = models.DateField(null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return str(self.backlog)
    

class Rol(models.Model):
    ROLES= (
        ('scrum_master', 'Scrum Master'),
        ('product_owner', 'Product Owner'),
        ('team_member', 'Team Member'),
    )
    descripcion = models.CharField(max_length=500, choices=ROLES)

    def __str__(self):
        return self.descripcion
    

class UsuProyRol(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username
    def get_rol(self):
        return self.rol.descripcion
    def get_proyecto(self):
        return self.proyecto.nombre
    

class Estados(models.Model):
    ESTADOS = (
        ('hacer', 'Por hacer'),
        ('proceso', 'En proceso'),
        ('terminado', 'Terminado'),
        ('cancelado', 'Cancelado')
    )
    estado = models.CharField(max_length=10, choices=ESTADOS)

    def __str__(self):
        return self.estado
    

class UserStory(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True, blank=True)
    usu_proy_rol = models.ForeignKey(UsuProyRol, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)
    story_points = models.IntegerField(null=True, blank=True)
    definicion_hecho = models.CharField(max_length=500, null=True, blank=True)
    prioridad = models.IntegerField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if not os.environ.get('ROLES_CREATED'):
        if not Rol.objects.filter(descripcion='Scrum Master').exists():
            Rol.objects.create(descripcion='Scrum Master')
        
        if not Rol.objects.filter(descripcion='Product Owner').exists():
            Rol.objects.create(descripcion='Product Owner')
        
        if not Rol.objects.filter(descripcion='Team Member').exists():
            Rol.objects.create(descripcion='Team Member')
        
        os.environ['ROLES_CREATED'] = 'True'

@receiver(post_migrate)
def create_estados(sender, **kwargs):
    if not os.environ.get('ESTADOS_CREATED'):
        if not Estados.objects.filter(estado='hacer').exists():
            Estados.objects.create(estado='hacer')
        
        if not Estados.objects.filter(estado='proceso').exists():
            Estados.objects.create(estado='proceso')
        
        if not Estados.objects.filter(estado='terminado').exists():
            Estados.objects.create(estado='terminado')

        if not Estados.objects.filter(estado='cancelado').exists():
            Estados.objects.create(estado='cancelado')
        
        os.environ['ESTADOS_CREATED'] = 'True'