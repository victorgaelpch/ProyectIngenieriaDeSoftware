from django import forms


class PedidoPickupForm(forms.Form):
    horario_recoleccion = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Horario de recolección"
    )
