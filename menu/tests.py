# menu/tests.py
from django.test import TestCase, skipUnlessDBFeature
from django_cassandra_engine.test import TestCase as CassandraTestCase
from .models import Categoria, Subcategoria, Producto
import uuid

class CategoriaModelTest(CassandraTestCase):
    def test_creacion_categoria(self):
        """Prueba la creación de una categoría en Cassandra"""
        categoria = Categoria.create(
            nombre='Bebidas',
            descripcion='Productos para beber',
            activo=True
        )
        
        self.assertEqual(categoria.nombre, 'Bebidas')
        self.assertTrue(categoria.activo)
        self.assertIsNotNone(categoria.id)

class SubcategoriaModelTest(CassandraTestCase):
    def setUp(self):
        self.categoria_id = uuid.uuid4()
        Categoria.create(
            id=self.categoria_id,
            nombre='Comidas',
            activo=True
        )
    
    def test_creacion_subcategoria(self):
        """Prueba la creación de una subcategoría en Cassandra"""
        subcategoria = Subcategoria.create(
            categoria_id=self.categoria_id,
            nombre='Postres',
            descripcion='Dulces y postres',
            activo=True
        )
        
        self.assertEqual(subcategoria.nombre, 'Postres')
        self.assertEqual(subcategoria.categoria_id, self.categoria_id)

class ProductoModelTest(CassandraTestCase):
    def setUp(self):
        self.categoria_id = uuid.uuid4()
        self.subcategoria_id = uuid.uuid4()
        
        Categoria.create(
            id=self.categoria_id,
            nombre='Bebidas',
            activo=True
        )
        Subcategoria.create(
            id=self.subcategoria_id,
            categoria_id=self.categoria_id,
            nombre='Cafés',
            activo=True
        )
    
    def test_creacion_producto(self):
        """Prueba la creación de un producto en Cassandra"""
        producto = Producto.create(
            categoria_id=self.categoria_id,
            subcategoria_id=self.subcategoria_id,
            nombre='Café Latte',
            descripcion='Café con leche espumosa',
            precio=45.00,
            stock=50,
            activo=True,
            atributos={'temperatura': 'caliente', 'tamaño': 'grande'}
        )
        
        self.assertEqual(producto.nombre, 'Café Latte')
        self.assertEqual(producto.precio, 45.00)
        self.assertEqual(producto.stock, 50)
        self.assertEqual(producto.atributos['temperatura'], 'caliente')