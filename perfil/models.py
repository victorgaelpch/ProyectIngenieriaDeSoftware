from django.db import models
from django.contrib.auth.models import User


class DireccionFacturacion(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='direcciones_facturacion')

    razon_social = models.CharField("Razón social", max_length=100)
    rfc = models.CharField("RFC", max_length=13)

    calle = models.CharField("Calle", max_length=100)
    numero_exterior = models.CharField("Número exterior", max_length=10)
    numero_interior = models.CharField(
        "Número interior", max_length=10, blank=True, null=True)

    colonia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50, default='México')
    cp = models.CharField("Código Postal", max_length=10)

    telefono_facturacion = models.CharField(
        "Teléfono de facturación", max_length=15)

    def __str__(self):
        return f'{self.razon_social} - {self.calle} #{self.numero_exterior}, {self.colonia}, {self.municipio}'
