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
        profile = Profile.objects.create(user=user, tlf=self.cleaned_data['tlf']) # Creamos un objeto Profile con los datos del modelo usuario y el campo adiciónal tlf
        return user





    