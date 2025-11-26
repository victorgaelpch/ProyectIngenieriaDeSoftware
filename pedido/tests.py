# pedido/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Sucursal, PerfilUsuario, Pedido, PedidoPickup, DetallePedido
from django.utils import timezone
from datetime import datetime
import uuid

class SucursalModelTest(TestCase):
    def test_creacion_sucursal(self):
        """Prueba la creación de una sucursal"""
        sucursal = Sucursal.objects.create(
            nombre_sucursal='Café Central',
            calle='Av. Reforma',
            numero_exterior='123',
            colonia='Centro',
            ciudad='CDMX',
            municipio='Cuauhtémoc',
            codigo_postal='06000',
            telefono='555-1234',
            hora_apertura='08:00:00',
            hora_cierre='20:00:00'
        )
        
        self.assertEqual(sucursal.nombre_sucursal, 'Café Central')
        self.assertEqual(str(sucursal), 'Café Central - Av. Reforma #123, Centro, CDMX')

class PerfilUsuarioModelTest(TestCase):
    def test_perfil_se_crea_automáticamente(self):
        """Prueba que el perfil se crea automáticamente al crear un usuario"""
        user = User.objects.create_user(
            username='usuarioprueba123',
            password='testpass123'
        )
        
        
        self.assertTrue(PerfilUsuario.objects.filter(user=user).exists())
        
        perfil = user.perfil  # Usando el related_name='perfil'
        self.assertEqual(perfil.nombre_usuario, '')  # Valor por defecto
        self.assertEqual(perfil.puntos, 0)  # Valor por defecto

class PedidoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.sucursal = Sucursal.objects.create(
            nombre_sucursal='Café Central',
            calle='Av. Reforma',
            numero_exterior='123',
            colonia='Centro',
            ciudad='CDMX',
            municipio='Cuauhtémoc',
            codigo_postal='06000',
            telefono='555-1234',
            hora_apertura='08:00:00',
            hora_cierre='20:00:00'
        )
    
    def test_creacion_pedido_con_codigo(self):
        """Prueba que el pedido se crea con un código único"""
        pedido = Pedido.objects.create(
            usuario=self.user,
            sucursal=self.sucursal,
            total=150.50
        )
        
        self.assertIsNotNone(pedido.codigo)
        self.assertEqual(len(pedido.codigo), 8)
        self.assertTrue(pedido.codigo.isupper())
    
    def test_pedido_estado_predeterminado(self):
        """Prueba que el estado predeterminado es 'pendiente'"""
        pedido = Pedido.objects.create(
            usuario=self.user,
            sucursal=self.sucursal,
            total=100.00
        )
        
        self.assertEqual(pedido.estado, 'pendiente')
    
    def test_pedido_sin_usuario(self):
        """Prueba pedido sin usuario (kiosko)"""
        pedido = Pedido.objects.create(
            sucursal=self.sucursal,
            total=75.00
        )
        
        self.assertIsNone(pedido.usuario)
        self.assertEqual(pedido.total, 75.00)

class PedidoPickupModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.sucursal = Sucursal.objects.create(
            nombre_sucursal='Café Central',
            calle='Av. Reforma',
            numero_exterior='123',
            colonia='Centro',
            ciudad='CDMX',
            municipio='Cuauhtémoc',
            codigo_postal='06000',
            telefono='555-1234',
            hora_apertura='08:00:00',
            hora_cierre='20:00:00'
        )
    
    from django.utils import timezone
from datetime import datetime

def test_creacion_pedido_pickup(self):
    """Prueba la creación de un pedido pickup"""
    pedido = Pedido.objects.create(
        usuario=self.user,
        sucursal=self.sucursal,
        total=200.00
    )
    
    # Usa timezone.now() para fechas con zona horaria
    horario = timezone.now().replace(hour=15, minute=30, second=0, microsecond=0)
    
    pickup = PedidoPickup.objects.create(
        pedido=pedido,
        horario_recoleccion=horario,  # Ahora es "aware"
        tipo_pago='efectivo'
    )
    
    self.assertEqual(pickup.pedido, pedido)
    self.assertEqual(pickup.tipo_pago, 'efectivo')
    
class DetallePedidoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.sucursal = Sucursal.objects.create(
            nombre_sucursal='Café Central',
            calle='Av. Reforma',
            numero_exterior='123',
            colonia='Centro',
            ciudad='CDMX',
            municipio='Cuauhtémoc',
            codigo_postal='06000',
            telefono='555-1234',
            hora_apertura='08:00:00',
            hora_cierre='20:00:00'
        )
        self.producto_id = uuid.uuid4()
    
    def test_creacion_detalle_pedido(self):
        """Prueba la creación de un detalle de pedido"""
        pedido = Pedido.objects.create(
            usuario=self.user,
            sucursal=self.sucursal,
            total=0
        )
        
        detalle = DetallePedido.objects.create(
            pedido=pedido,
            producto_id=self.producto_id,
            cantidad=2,
            nombre_producto='Café Americano',
            precio_unitario=35.00
        )
        
        self.assertEqual(detalle.cantidad, 2)
        self.assertEqual(detalle.precio_unitario, 35.00)
        self.assertEqual(detalle.subtotal, 70.00)
        self.assertEqual(detalle.nombre_producto, 'Café Americano')