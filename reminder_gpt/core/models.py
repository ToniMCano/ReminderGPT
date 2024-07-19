
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_phone(value):
    
    if len(value) != 9 or not value.isdigit():
        
        raise ValidationError('El número debe tener exactamente 9 dígitos.')


class Profile(models.Model):   # Lo usaremos para extedner el modelo usuario con el teléfono
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relaciona user con la clase User
    tlf = models.CharField(max_length = 9)

    def __str__(self):
        return f'Crado Usuario: {self.user.username}'
