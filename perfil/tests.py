from django.test import TestCase
from django.contrib.auth.models import User
from .models import DireccionFacturacion

class DireccionFacturacionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_creacion_direccion(self):
        """Prueba la creación de una dirección de facturación"""
        direccion = DireccionFacturacion.objects.create(
            usuario=self.user,
            razon_social='Test SA de CV',
            rfc='TEST123456ABC',
            calle='Av. Principal',
            numero_exterior='123',
            colonia='Centro',
            municipio='Ciudad',
            estado='Estado',
            cp='12345',
            telefono_facturacion='555-1234'
        )
        
        self.assertEqual(direccion.razon_social, 'Test SA de CV')
        self.assertEqual(direccion.usuario, self.user)
        self.assertEqual(str(direccion), 'Test SA de CV - Av. Principal #123, Centro, Ciudad')
    
    def test_direccion_con_numero_interior(self):
        """Prueba dirección con número interior"""
        direccion = DireccionFacturacion.objects.create(
            usuario=self.user,
            razon_social='Test SA de CV',
            rfc='TEST123456ABC',
            calle='Av. Principal',
            numero_exterior='123',
            numero_interior='A',
            colonia='Centro',
            municipio='Ciudad',
            estado='Estado',
            cp='12345',
            telefono_facturacion='555-1234'
        )
        
        self.assertEqual(direccion.numero_interior, 'A')