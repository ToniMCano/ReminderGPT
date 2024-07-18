from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  # Importamos el perfil personalizado.




class SignUpForm(UserCreationForm):
    
    tlf = forms.CharField(max_length=9, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tlf')

    def clean_tlf(self):
        tlf = self.cleaned_data.get('tlf')
        
        if not tlf.isdigit():
            raise forms.ValidationError("El tlf debe contener solo números.")

        if len(tlf) != 9:
            raise forms.ValidationError("El tlf debe tener exactamente 9 dígitos.")
        
        return tlf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        # Verificar si el usuario ya tiene un perfil asociado
        #if hasattr(user, 'profile'):
            # Si el perfil ya existe, lanzar un error o manejar la situación según tu lógica de negocio
            #print("Este usuario ya tiene un perfil asociado.")
        
        # Crear el perfil asociado al usuario
        profile = Profile.objects.create(user=user, tlf=self.cleaned_data['tlf'])
        print(profile)

        print(profile.user)

        print(profile.tlf)

        return user



    