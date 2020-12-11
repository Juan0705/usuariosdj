from django import forms
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir contraseña'
            }
        )
    )
    
    class Meta:
        model = User
        #fields = ('__all__') # trae todos los campos
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
        )

    # validador de contraseña en la vista
    def clean_password2(self):
    
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son las mismas')

#'form.Form' permite crear un formulario sin depender de un modelo
class LoginForm(forms.Form):
    username = forms.CharField(
        label='username ', 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username '
            }
        )
    )

    password = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        # si el usuario no esta autenticado
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos del usuario no son correctos')

        return self.cleaned_data

    
class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña Actrual'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña Nueva'
            }
        )
    )

class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)

    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']
    
        if len(codigo) == 6:
            # verificamos si el codigo y el id de usuario son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:# si activo es False
                raise forms.ValidationError('El codigo es incorrectos')
        else:
            raise forms.ValidationError('El codigo debe tener 6 caracteres')
    
        return codigo
