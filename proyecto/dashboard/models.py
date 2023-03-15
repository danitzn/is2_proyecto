from django.db import models
from login.models import User

# Create your models here.
class Project(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    
class Sprint(models.Model):
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre
    

class Task(models.Model):
    SPRINT_ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('terminada', 'Terminada'),
    ]
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=SPRINT_ESTADOS, default='pendiente')

    def __str__(self):
        return self.nombre
    



