from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Receta(models.Model):
     nombre = models.CharField(max_length=50)
     ingredientes = models.CharField(max_length=250)
     instrucciones = models.CharField(max_length=250)
     fecha_de_creacion = models.DateTimeField(auto_now_add = True)
     autor = models.ForeignKey(User, on_delete = models.CASCADE)
     imagen = models.ImageField(upload_to='imagenes_recetas/', null=True, blank=True)
     
     def __str__(self):
         return self.nombre