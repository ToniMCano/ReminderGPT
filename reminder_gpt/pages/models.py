
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Registry(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(verbose_name = "Nombre del Proyecto", max_length=50)
    user = models.ForeignKey(User , verbose_name = "Usuario" , on_delete = models.CASCADE , default = None)
    log = models.TextField(verbose_name = "Log" , default = None)
    #email = models.EmailField(max_length=254 , unique = True , default = "provwork@gmail.com") 
    #phone = models.CharField(verbose_name="Teléfono", max_length=9, validators=[validate_phone] , unique = True ,  default = 123456789)  
    created = models.DateField(auto_now_add = True , verbose_name = 'Fecha de Creación')
    updated = models.DateField(auto_now = True , verbose_name = 'Fecha de Actualización')

    class Meta:

        verbose_name = "registro"
        verbose_name_plural = "registros"

        ordering = ["project_name"]

    def __str__(self):

        return self.project_name
    