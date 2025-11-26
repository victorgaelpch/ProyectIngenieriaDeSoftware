# administracion/tests.py
from django.test import TestCase
from .models import SiteTheme

class SiteThemeModelTest(TestCase):
    def test_creacion_tema_predeterminado(self):
        """Prueba la creación de un tema con valores predeterminados"""
        tema = SiteTheme.objects.create(
            name='tema_prueba'
        )
        
        self.assertEqual(tema.name, 'tema_prueba')
        self.assertEqual(tema.primary_color, '#667eea')
        self.assertEqual(tema.secondary_color, '#48bb78')
        self.assertEqual(tema.border_radius, 'normal')
        self.assertEqual(tema.shadow_intensity, 'medium')
        self.assertTrue(tema.is_active)
    
    def test_conversion_a_diccionario(self):
        """Prueba la conversión del tema a diccionario"""
        tema = SiteTheme.objects.create(
            name='tema_test',
            primary_color='FF0000',
            secondary_color='00FF00'
        )
        
        tema_dict = tema.to_dict()
        
        self.assertEqual(tema_dict['primaryColor'], '#ff0000')
        self.assertEqual(tema_dict['secondaryColor'], '#00ff00')
    
    def test_obtener_tema_activo(self):
        """Prueba obtener el tema activo"""
        # Desactivar cualquier tema existente
        SiteTheme.objects.update(is_active=False)
        
        # Crear un nuevo tema activo
        tema_activo = SiteTheme.objects.create(
            name='activo',
            is_active=True
        )
        
        # Crear un tema inactivo
        SiteTheme.objects.create(
            name='inactivo',
            is_active=False
        )
        
        tema_obtenido = SiteTheme.get_active_theme()
        self.assertEqual(tema_obtenido, tema_activo)