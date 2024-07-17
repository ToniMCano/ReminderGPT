from django.shortcuts import render
from django.contrib.auth.models import User
from . models import Registry

# Create your views here.

def home(request):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        user = request.user
    else:
        #  HAY QUE REDIRIGIR A UNA PÁGINA DE REGISTRO.
        #user, created = User.objects.get_or_create(username='new_user', defaults={'password': 'password'}) Si no hay un usuario autenticado, crea un nuevo usuario de prueba -
        pass

    # Crea un nuevo registro
    new_registry = Registry.objects.create(
        project_name='test_name',
        user=user,
        Log='test_log'
    )

    return render(request, 'core/index.html')

user, created = User.objects.get_or_create(username='new_user')

# Establecer la contraseña de manera segura
user.set_password('password')
user.save()