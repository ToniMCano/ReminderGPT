"""
Este módulo contiene las vistas para la aplicación principal, gestionando la autenticación de usuarios y el registro.

Las funciones incluidas son:

- home(request): Renderiza la página de inicio y maneja el formulario de inicio de sesión.
- sign_up(request): Renderiza la página de registro de usuario y maneja el formulario de registro.
- create_user(request): Renderiza la página de creación de usuario con el formulario de registro.

Cada vista procesa las solicitudes HTTP y devuelve respuestas HTTP correspondientes, incluyendo la lógica para autenticación de usuarios y gestión de formularios.

Importaciones:
- django.shortcuts: Utilizado para renderizar plantillas y redirigir vistas.
- django.contrib.auth.models: Modelos de autenticación proporcionados por Django.
- django.contrib.auth: Funciones de autenticación proporcionadas por Django.
- .forms: Formularios personalizados para el inicio de sesión y registro de usuarios.
- django.urls: Herramientas para la gestión de rutas URL.
- django.http: Utilizado para generar respuestas HTTP.

Uso:
Estas vistas son utilizadas en las plantillas de la aplicación principal para gestionar la autenticación y el registro de usuarios, proporcionando una interfaz sencilla y segura para los usuarios de la aplicación.
"""
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate
from .forms import SignUpForm , LoginForm
from django.urls import path , reverse
from django.http import HttpResponse


# Create your views here.


def home(request): 
    
    form = LoginForm() 
    
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['user'] # cleaned_data es un diccionario dónde se almacenan los valores capturados en el formulario.
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password) # Comprueba que el usuario existe y la contraseña coincide
            
            if user is not None:
                login(request, user)
                
                return redirect('chat')  
            
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')

    return render(request, 'core/index.html', {'form': form , 'title':"Home"})
    
        
def sign_up(request):
    """
    Renderiza la página de registro de usuario y maneja el formulario de registro.

    Args:
    request (HttpRequest): La solicitud HTTP.

    Returns:
    HttpResponse: La respuesta HTTP con el formulario de registro y un indicador de validez.
    Si nos válido muestra un mensaje en el FrontEnd.
    """
     
    form = SignUpForm()
    not_valid = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()

            return redirect('home')  
        
        else:
            not_valid = True # Afinar para mandar información sobre que es lo que no es correcto.
 

    return render(request, "core/create_user.html", {'form': form , "not_valid": not_valid})


def create_user(request):
    """
    Renderiza la página de creación de usuario con el formulario de registro.

    Args:
    request (HttpRequest): La solicitud HTTP.

    Returns:
    HttpResponse: La respuesta HTTP con el formulario de registro.
    """
    
    form = SignUpForm()
    
    return render(request , "core/create_user.html" , {'form':form})

 
        
        
        
