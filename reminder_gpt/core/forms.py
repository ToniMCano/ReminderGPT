from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User , Group
from .models import Profile  


class SignUpForm(UserCreationForm):
    
    tlf = forms.CharField(max_length=9, required=True)


    class Meta:
        
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tlf') # sobreescribe los campos del modelo User antes serían   ('username', 'email', 'password1', 'password2')


    def clean_tlf(self): # clean_nombre_del_campo se ejecuta con.is_valid()
        
        tlf = self.cleaned_data.get('tlf')
        
        if not tlf.isdigit():
            raise forms.ValidationError("El tlf debe contener solo números.")

        if len(tlf) != 9:
            raise forms.ValidationError("El tlf debe tener exactamente 9 dígitos.")
        
        return tlf


    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.save()

        profile = Profile.objects.create(user=user, tlf=self.cleaned_data['tlf']) # Crear el perfil asociado al usuario
        
        group_name = 'basic_user'  
        group, created = Group.objects.get_or_create(name=group_name)
        
        user.groups.add(group)

        return user


class LoginForm(forms.Form):
    
    user = forms.CharField(label = "Usuario", max_length= 100 , required = True)
    password = forms.CharField(label = "Password", widget=forms.PasswordInput , required = True)
    
    
    
    


    