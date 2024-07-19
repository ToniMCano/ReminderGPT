from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate
from .forms import SignUpForm , LoginForm
from django.urls import path


# Create your views here.


def home(request): # Es una prueba (SignUpForm registra usuarios),  hay que hacer un formulario para esta función.
    
    form = LoginForm() 
    
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['user'] # cleaned_data es un diccionario dónde se almacenan los valores capturados en el formulario.
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                return redirect('test')  
            
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
                
                user = form.save() # Procesar formulario y guardar usuario
                
               #  login(request, user) iniciar sesión automáticamente después del registro
               
                return redirect('index')
            
        else:
            return render(request, "core/create_user.html")