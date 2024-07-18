from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_phone(value):
    
    if len(value) != 9 or not value.isdigit():
        
        raise ValidationError('El número debe tener exactamente 9 dígitos.')


class Registry(models.Model):

    project_name = models.CharField(verbose_name = "Nombre del Proyecto", max_length=50)
    user = models.ForeignKey(User , verbose_name = "Usuario" , on_delete = models.CASCADE , default = None)
    Log = models.TextField(verbose_name = "Log" , default = None)
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
    
    

class Profile(models.Model):   # Lo usaremos para extedner el modelo usuario con el teléfono
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relaciona user con la clase User
    tlf = models.CharField(max_length = 9)

    def __str__(self):
        return f'Crado Usuario: {self.user.username}'
