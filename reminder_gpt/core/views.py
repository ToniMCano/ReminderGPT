from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from .new_user_form import SignUpForm

# Create your views here.


def home(request): # Es una prueba (SignUpForm registra usuarios),  hay que hacer un formulario para esta función.
    
    form = SignUpForm() 
   
    return render(request , 'core/index.html', {'form' : form})
    
    
def signup(request):
    
    new_user_form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Puedes redirigir a cualquier URL que desees aquí
            return redirect('registro_exitoso')  # Redirigir a la página de registro exitoso
    else:
        form = SignUpForm()
    
    return render(request, "core/create_user.html" , {'form' : new_user_form})


def sing_in(request):
    
    if User.objects.filter(username = 'Toni').exists():
        print("Toni Existe")
    
    
    if request.user.is_authenticated: # Verifica si el usuario está autenticado
        user = request.user
        return render(request , "core/test.html" , {'user' : user , 'message' : 'eres un usuario válido.' }) # Redirigir a sus logs
    
    else:
        return render(request , "core/create_user.html") # Redirigir a signup
