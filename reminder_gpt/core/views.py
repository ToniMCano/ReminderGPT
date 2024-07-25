from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate
from .forms import SignUpForm , LoginForm
from django.urls import path , reverse


# Create your views here.


def home(request): # Es una prueba (SignUpForm registra usuarios),  hay que hacer un formulario para esta función.
    
    form = LoginForm() 
    
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['user'] # cleaned_data es un diccionario dónde se almacenan los valores capturados en el formulario.
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password) # Comprueba que el usuario existe y la contraseña coincide
            
            if user is not None:
                login(request, user)
                
                return redirect(reverse('chat'))  
            
            else:
                form.add_error(None, 'Usuario o contrasesña incorrectos')
    
    return render(request, 'core/index.html', {'form': form})
    
    
def test(request):
    
    return render(request , "core/test.html")
    
    
def sign_up(request):
     
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
    
    form = SignUpForm()
    
    return render(request , "core/create_user.html" , {'form':form})



        
        
        
        
