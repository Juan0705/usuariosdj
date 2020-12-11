from django.db import models

from django.contrib.auth.models  import AbstractBaseUser, PermissionsMixin

#
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )


    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    nombres = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    codregistro = models.CharField(max_length=6, blank=True) # codigo de registro

    # puede o no puede acceder a la pagina de administrador de django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    #al crear usuario pide este campo
    USERNAME_FIELD = 'username'

    #al crear usuario pide este campo
    REQUIRED_FIELDS = ['email',]

    objects = UserManager()
    
    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.nombres + ' ' +self.apellidos

