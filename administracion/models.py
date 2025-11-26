from django.db import models
import json
# Create your models here.
# models.py
class SiteTheme(models.Model):
    name = models.CharField(max_length=100, default='default')
    
    # Colores primarios
    primary_color = models.CharField(max_length=7, default='#667eea')
    primary_dark = models.CharField(max_length=7, default='#764ba2')
    primary_light = models.CharField(max_length=7, default='#a8b9ff')
    
    # Colores secundarios
    secondary_color = models.CharField(max_length=7, default='#48bb78')
    secondary_dark = models.CharField(max_length=7, default='#38a169')
    secondary_light = models.CharField(max_length=7, default='#9ae6b4')
    
    # Colores de estado
    success_color = models.CharField(max_length=7, default='#48bb78')
    success_bg = models.CharField(max_length=7, default='#c6f6d5')
    success_dark = models.CharField(max_length=7, default='#2f855a')
    
    error_color = models.CharField(max_length=7, default='#e53e3e')
    error_bg = models.CharField(max_length=7, default='#fed7d7')
    error_dark = models.CharField(max_length=7, default='#c53030')
    
    warning_color = models.CharField(max_length=7, default='#ed8936')
    warning_bg = models.CharField(max_length=7, default='#ffd89a')
    warning_dark = models.CharField(max_length=7, default='#c05621')
    
    info_color = models.CharField(max_length=7, default='#3182ce')
    info_bg = models.CharField(max_length=7, default='#bee3f8')
    info_dark = models.CharField(max_length=7, default='#2b6cb0')
    
    border_radius = models.CharField(
        max_length=20,
        choices=[
            ('sharp', 'Bordes Rectos'),
            ('normal', 'Bordes Normales'),
            ('rounded', 'Bordes Redondeados')
        ],
        default='normal'
    )
    shadow_intensity = models.CharField(
        max_length=20,
        choices=[
            ('light', 'Suaves'),
            ('medium', 'Normales'),
            ('strong', 'Fuertes')
        ],
        default='medium'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_active', '-updated_at']
    
    def __str__(self):
        return f"Tema: {self.name}"
    
    def to_dict(self):
        """Convertir a diccionario para JavaScript"""
        return {
            # Colores primarios
            'primaryColor': f"#{self.primary_color.lower()}",
            'primaryDark': f"#{self.primary_dark.lower()}",
            'primaryLight': f"#{self.primary_light.lower()}",
            
            # Colores secundarios
            'secondaryColor': f"#{self.secondary_color.lower()}",
            'secondaryDark': f"#{self.secondary_dark.lower()}",
            'secondaryLight': f"#{self.secondary_light.lower()}",
            
            # Colores de estado
            'successColor': f"#{self.success_color.lower()}",
            'successBg': f"#{self.success_bg.lower()}",
            'successDark': f"#{self.success_dark.lower()}",
            
            'errorColor': f"#{self.error_color.lower()}",
            'errorBg': f"#{self.error_bg.lower()}",
            'errorDark': f"#{self.error_dark.lower()}",
            
            'warningColor': f"#{self.warning_color.lower()}",
            'warningBg': f"#{self.warning_bg.lower()}",
            'warningDark': f"#{self.warning_dark.lower()}",
            
            'infoColor': f"#{self.info_color.lower()}",
            'infoBg': f"#{self.info_bg.lower()}",
            'infoDark': f"#{self.info_dark.lower()}",
            
            'borderRadius': self.border_radius,
            'shadowIntensity': self.shadow_intensity
        }
    
    def to_json(self):
        """Convertir a JSON string"""
        import json
        return json.dumps(self.to_dict())
    
    @classmethod
    def get_active_theme(cls):
        """Obtener el tema activo actual"""
        return cls.objects.filter(is_active=True).first()