from django import forms
from pedido.models import Sucursal


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = '__all__'
        widgets = {
            'hora_apertura': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_cierre': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
