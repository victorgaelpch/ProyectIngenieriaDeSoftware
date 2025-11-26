# perfil/forms.py
from django.contrib.auth.models import User
from django import forms
from pedido.models import PerfilUsuario
from perfil.models import DireccionFacturacion  # o donde tengas este modelo


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = [
            'nombre_usuario',
            'apellido_pat_usuario',
            'apellido_mat_usuario',
            'estado_notificaciones',
            'telefono',
            'fecha_nacimiento',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class DireccionFacturacionForm(forms.ModelForm):
    class Meta:
        model = DireccionFacturacion
        exclude = ['usuario']  # Se asigna en la vista
