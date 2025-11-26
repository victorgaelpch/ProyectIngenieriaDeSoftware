
from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Sucursal(models.Model):
    nombre_sucursal = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10, blank=True, null=True)
    colonia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    telefono = models.CharField(max_length=20)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()

    def __str__(self):
        return f'{self.nombre_sucursal} - {self.calle} #{self.numero_exterior}, {self.colonia}, {self.ciudad}'


class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil')
    nombre_usuario = models.CharField(max_length=50, default='')
    apellido_pat_usuario = models.CharField(max_length=50)
    apellido_mat_usuario = models.CharField(max_length=50)
    estado_cuenta_usuario = models.CharField(max_length=20, default='activo')
    estado_notificaciones = models.BooleanField(default=True)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    puntos = models.PositiveIntegerField(default=0)
    id_gestor_pagos_online = models.CharField(
        max_length=100, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'


class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('preparando', 'Preparando'),
        ('listo', 'Listo para recoger'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    codigo = models.CharField(
        max_length=12, unique=True, blank=True, null=True)
    usuario = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default='pendiente')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    puntos_ganados = models.PositiveIntegerField(default=0)
    puntos_usados = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.username} ({self.get_estado_display()})'


class PedidoPickup(models.Model):
    pedido = models.OneToOneField(
        Pedido, on_delete=models.CASCADE, related_name='pickup')
    horario_recoleccion = models.DateTimeField()
    tipo_pago = models.CharField(max_length=20, choices=[(
        'tarjeta', 'Tarjeta'), ('efectivo', 'Efectivo')])


class PedidoKiosko(models.Model):
    pedido = models.OneToOneField(
        Pedido, on_delete=models.CASCADE, related_name='kiosko')

    metodo_confirmacion = models.CharField(max_length=50)


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto_id = models.UUIDField(
        default=uuid.uuid4,
        help_text="UUID del producto en Cassandra"
    )
    
    cantidad = models.PositiveIntegerField(default=1)
    # Campos de caché del producto
    nombre_producto = models.CharField(
        max_length=255, 
        default='Producto sin nombre'
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f'{self.cantidad} x {self.nombre_producto} (Pedido #{self.pedido.id})'

    def save(self, *args, **kwargs):
        from menu.models import Producto
        # Actualizar información del producto desde Cassandra
        try:
            producto = Producto.objects.get(id=self.producto_id)
            self.nombre_producto = producto.nombre
            self.precio_unitario = producto.precio
        except Producto.DoesNotExist:
            pass
        
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)