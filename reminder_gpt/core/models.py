
"""
Módulo que gestiona los modelos de la aplicación, incluyendo la validación y extensión del modelo de usuario.

Este módulo incluye las siguientes clases y funciones:

Clases:
- Profile: Extiende el modelo de usuario con un número de teléfono.

Funciones:
- validate_phone(value): Valida que el número de teléfono tenga exactamente 9 dígitos y contenga solo números.

Importaciones:
- django.db.models: Utilizado para definir modelos en Django.
- django.utils.timezone.now: Utilizado para trabajar con fechas y horas.
- django.contrib.auth.models.User: Modelo de usuario proporcionado por Django.
- django.core.exceptions.ValidationError: Utilizado para manejar errores de validación.

Uso:
Este módulo se utiliza para definir y manejar los datos adicionales del perfil del usuario, específicamente el número de teléfono, y para validar estos datos.
"""
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_phone(value):  #TODO No lo puedo eliminar porque está incluido en todas las migraciones, cuando el proyecto esté terminado lo eliminaré y reinciciaré el proyecto.
    """
    Valida que el número de teléfono tenga exactamente 9 dígitos y contenga solo números.

    Args:
    value (str): El número de teléfono a validar.

    Raises:
    ValidationError: Si el número de teléfono no tiene exactamente 9 dígitos o contiene caracteres no numéricos.
    """
    
    if len(value) != 9 or not value.isdigit():
        
        raise ValidationError('El número debe tener exactamente 9 dígitos.')


class Profile(models.Model):   # Lo usaremos para extedner el modelo usuario con el teléfono
    """
    Clase Profile
    Extiende el modelo de usuario con un número de teléfono.

    Args:
    user (User): Relaciona el perfil con un objeto de la clase User.
    tlf (str): El número de teléfono del usuario (debe tener exactamente 9 dígitos).

    Methods:
    __str__(): Retorna una cadena que representa el perfil del usuario.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relaciona user con la clase User
    tlf = models.CharField(max_length = 9)

    def __str__(self):
        return f'Crado Usuario: {self.user.username}'
    
    """
    Retorna una cadena que representa el perfil del usuario.

    Returns:
    str: Una cadena que incluye el nombre de usuario.
    """
