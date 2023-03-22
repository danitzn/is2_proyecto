from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Correo electrónico', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='Nombre', max_length=30)
    last_name = models.CharField(verbose_name='Apellido', max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

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

