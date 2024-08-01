"""
Módulo que define los formularios utilizados en la aplicación para la creación y autenticación de usuarios.

Este módulo incluye las siguientes clases:

Clases:
- SignUpForm: Formulario para registrar un nuevo usuario, incluyendo un número de teléfono.
- LoginForm: Formulario para que un usuario inicie sesión.

Importaciones:
- django.forms: Utilizado para definir los campos del formulario.
- django.contrib.auth.forms.UserCreationForm: Utilizado como base para el formulario de registro de usuarios.
- django.contrib.auth.models.User, Group: Modelos de usuario y grupo proporcionados por Django.
- .models.Profile: Modelo de perfil de usuario extendido con un número de teléfono.

Uso:
Este módulo se utiliza para gestionar los formularios de registro y autenticación de usuarios, validando los datos introducidos y asociando perfiles y grupos a los usuarios creados.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User , Group
from .models import Profile  


class SignUpForm(UserCreationForm):
    
    """
    Clase SignUpForm
    Incluye los campos necesarios para registrar un nuevo usuario, incluyendo un número de teléfono. 
    Por defecto, todos los campos son obligatorios.

    Args:
    username : Es un string que compone el nombre de usuario.
    email : Es un string que compone el correo electrónico del usuario.
    password1 : Es un string que compone la primera entrada de la contraseña del usuario.
    password2 : Es un string que compone la segunda entrada de la contraseña del usuario para verificarla.
    tlf : Es un string que compone el número de teléfono del usuario (debe ser numérico y tener exactamente 9 dígitos).
    
    Methods:
    clean_tlf: Comprueba que el teléfono solo contenga números y que la longitud sea de 9 dígitos.
    save: Guarda el usuario creado y le asigna un perfil y grupo.
    """

    
    tlf = forms.CharField(max_length=9, required=True)


    class Meta:
        
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tlf') # sobreescribe los campos del modelo User antes serían   ('username', 'email', 'password1', 'password2')


    def clean_tlf(self): # clean_nombre_del_campo se ejecuta con.is_valid()
            
        """
        Comprueba que el teléfono solo contenga números y que la longitud sea de 9 dígitos.

        Raises:
        forms.ValidationError: Si el teléfono contiene caracteres no numéricos o no tiene exactamente 9 dígitos.

        Returns:
        str: El número de teléfono validado.
        """
        
        tlf = self.cleaned_data.get('tlf')
        
        if not tlf.isdigit():
            raise forms.ValidationError("El tlf debe contener solo números.")

        if len(tlf) != 9:
            raise forms.ValidationError("El tlf debe tener exactamente 9 dígitos.")
        
        return tlf


    def save(self, commit=True):
        """
        Guarda el usuario creado y le asigna un perfil y grupo.

        Crea un usuario, su perfil asociado con el número de teléfono, y lo añade a un grupo predeterminado.

        Args:
        commit (bool): Indica si el objeto debe ser guardado en la base de datos inmediatamente.

        Returns:
        User: El usuario creado.
        """
        
        user = super().save(commit=False)
        user.save()

        profile = Profile.objects.create(user=user, tlf=self.cleaned_data['tlf']) # Crear el perfil asociado al usuario
        
        group_name = 'basic_user'  
        group, created = Group.objects.get_or_create(name=group_name)
        
        user.groups.add(group)

        return user


class LoginForm(forms.Form):
    """
    Clase LoginForm
    Incluye los campos necesarios para que un usuario inicie sesión.

    Args:
    user : Es un string que compone el nombre de usuario.
    password : Es un string que compone la contraseña del usuario.
    """
    
    user = forms.CharField(label = "Usuario", max_length= 100 , required = True)
    password = forms.CharField(label = "Password", widget=forms.PasswordInput , required = True)
    
    
    
    


    