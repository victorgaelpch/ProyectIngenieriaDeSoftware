from .models import SiteTheme

# context_processors.py o en tu views.py
def theme_context(request):
    """Context processor para agregar el tema activo a todas las plantillas"""
    from .models import SiteTheme  # Asegúrate de importar tu modelo
    
    active_theme = SiteTheme.get_active_theme()
    
    # Generar CSS inline con las variables personalizadas
    theme_css = ""
    if active_theme:
        # Asegurarse de que los colores tengan el formato correcto
        primary_color = f"#{active_theme.primary_color.lower()}"
        primary_dark = f"#{active_theme.primary_dark.lower()}"
        primary_light = f"#{active_theme.primary_light.lower()}"
        secondary_color = f"#{active_theme.secondary_color.lower()}"
        secondary_dark = f"#{active_theme.secondary_dark.lower()}"
        secondary_light = f"#{active_theme.secondary_light.lower()}"
        success_color = f"#{active_theme.success_color.lower()}"
        success_bg = f"#{active_theme.success_bg.lower()}"
        success_dark = f"#{active_theme.success_dark.lower()}"
        error_color = f"#{active_theme.error_color.lower()}"
        error_bg = f"#{active_theme.error_bg.lower()}"
        error_dark = f"#{active_theme.error_dark.lower()}"
        warning_color = f"#{active_theme.warning_color.lower()}"
        warning_bg = f"#{active_theme.warning_bg.lower()}"
        warning_dark = f"#{active_theme.warning_dark.lower()}"
        info_color = f"#{active_theme.info_color.lower()}"
        info_bg = f"#{active_theme.info_bg.lower()}"
        info_dark = f"#{active_theme.info_dark.lower()}"

        # Mapeo de bordes y sombras
        border_radius_map = {
            'sharp': {'sm': '4px', 'md': '6px', 'lg': '8px', 'xl': '10px'},
            'normal': {'sm': '8px', 'md': '12px', 'lg': '15px', 'xl': '20px'},
            'rounded': {'sm': '12px', 'md': '16px', 'lg': '20px', 'xl': '25px'}
        }
        
        shadow_map = {
            'light': {
                'sm': '0 1px 2px rgba(0,0,0,0.03)',
                'md': '0 2px 8px rgba(0,0,0,0.05)',
                'lg': '0 5px 15px rgba(0,0,0,0.07)',
                'xl': '0 10px 25px rgba(0,0,0,0.1)'
            },
            'medium': {
                'sm': '0 2px 4px rgba(0,0,0,0.05)',
                'md': '0 4px 12px rgba(0,0,0,0.08)',
                'lg': '0 10px 30px rgba(0,0,0,0.1)',
                'xl': '0 20px 40px rgba(0,0,0,0.15)'
            },
            'strong': {
                'sm': '0 3px 6px rgba(0,0,0,0.08)',
                'md': '0 6px 16px rgba(0,0,0,0.12)',
                'lg': '0 12px 35px rgba(0,0,0,0.15)',
                'xl': '0 25px 50px rgba(0,0,0,0.2)'
            }
        }
        
        radii = border_radius_map.get(active_theme.border_radius, border_radius_map['normal'])
        shadows = shadow_map.get(active_theme.shadow_intensity, shadow_map['medium'])
        
        theme_css = f"""
        :root {{
            /* Colores Primarios */
            --primary-color: {primary_color};
            --primary-dark: {primary_dark};
            --primary-light: {primary_light};
            --primary-gradient: linear-gradient(135deg, {primary_color} 0%, {primary_dark} 100%);
            
            /* Colores Secundarios */
            --secondary-color: {secondary_color};
            --secondary-dark: {secondary_dark};
            --secondary-light: {secondary_light};
            
            /* Colores de Estado */
            --success-color: {success_color};
            --success-bg: {success_bg};
            --success-dark: {success_dark};
            --error-color: {error_color};
            --error-bg: {error_bg};
            --error-dark: {error_dark};
            --warning-color: {warning_color};
            --warning-bg: {warning_bg};
            --warning-dark: {warning_dark};
            --info-color: {info_color};
            --info-bg: {info_bg};
            --info-dark: {info_dark};
            
            /* Bordes */
            --radius-sm: {radii['sm']};
            --radius-md: {radii['md']};
            --radius-lg: {radii['lg']};
            --radius-xl: {radii['xl']};
            
            /* Sombras */
            --shadow-sm: {shadows['sm']};
            --shadow-md: {shadows['md']};
            --shadow-lg: {shadows['lg']};
            --shadow-xl: {shadows['xl']};
        }}
        """
    
    return {
        'active_theme': active_theme,
        'theme_css': theme_css,
        'theme_json': active_theme.to_json() if active_theme else '{}'
    }