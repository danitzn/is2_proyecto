from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre
    
    
class Sprint(models.Model):
    backlog = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre
    

class Rol(models.Model):
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre
    

class UsuProyRol(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Estados(models.Model):
    ESTADOS = (
        ('hacer', 'Por hacer'),
        ('proceso', 'En proceso'),
        ('terminado', 'Terminado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS)

    def __str__(self):
        return self.nombre
      

class UserStory(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    usu_proy_rol = models.ForeignKey(UsuProyRol, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

