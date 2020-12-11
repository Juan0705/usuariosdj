from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic import (
    CreateView,
    View,
)

from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserRegisterForm, 
    LoginForm, 
    UpdatePasswordForm,
    VerificationForm
)

from .models import User

from .functions import code_generator


class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        
        #generamos codigo de verificacion
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],# recupera los datos del formulario
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo # asignar un codigo
        )

        #enviar el codigo al email del usuario
        asunto = 'Confirmacion de email'
        mensaje = 'Codigo de verificacion: ' + codigo
        email_remitente = 'jsepulveda0705@gmail.com'
        #
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        #redirige a pantalla de validacion
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk':usuario.id}# redirige a pantalla conservando al usuario
            )
        )

        '''
        return super(UserRegisterView, self).form_valid(form)
        '''

class LoginUser(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel') # 'reverse_lazy' permite acceder a urls de otras aplicaciones

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = "users/login.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login') # 'reverse_lazy' permite acceder a urls de otras aplicaciones
    login_url = reverse_lazy('users_app:user-login') # 'login_url' solo ingresa a esta pantalla (/update) los usuarios logeados

    def form_valid(self, form):
        #recuperar usuario activo
        usuario = self.request.user
        #hacer autenticacion
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )
        # si la autentificacion es correcta
        if user:
            # autualiza el nuevo password
            new_password = form.cleaned_data['password2'] # recupera password nuevo
            usuario.set_password(new_password) # establece el nuevo password
            usuario.save() # guarda los datos del nuevo password
        # cierra la sesion
        logout(self.request)
        
        return super(UpdatePasswordView, self).form_valid(form)

#verifica clave de autentificacion
class CodeVerificationView(FormView):
    template_name = "users/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login') 

    def get_form_kwargs(self):#########################
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):#################33
        #
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(CodeVerificationView, self).form_valid(form)






