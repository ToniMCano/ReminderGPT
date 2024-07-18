from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .new_user_form import SignUpForm
from django.urls import path


# Create your views here.


def home(request): # Es una prueba (SignUpForm registra usuarios),  hay que hacer un formulario para esta función.
    
    form = SignUpForm() 
   
    return render(request , 'core/index.html', {'form' : form})
    
    
def validate(request):
    
    return redirect('sign_up')
    
    
def sign_up(request):
     
    form = SignUpForm()
    not_valid = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Loguea al usuario inmediatamente después de registrarse 
            #login(request, user)

            return redirect('home')  
        
        else:
            not_valid = True 
 

    return render(request, "core/create_user.html", {'form': form , "not_valid": not_valid})


def sing_in(request):
    
    if User.objects.filter(username='Toni').exists():
        print("Toni Existe")
    
    if request.user.is_authenticated:
        user = request.user
        
        return render(request, "core/test.html", {'user': user, 'message': 'Eres un usuario válido.'})
    
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                # Procesar formulario y guardar usuario
                user = form.save()
                # Opcional: iniciar sesión automáticamente después del registro
                login(request, user)
               
                return redirect('index')
            
        else:
            return render(request, "core/create_user.html")