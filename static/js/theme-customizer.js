// theme-customizer.js
class ThemeCustomizer {
    constructor() {
        this.defaultTheme = {
            primaryColor: '#667eea',
            primaryDark: '#764ba2',
            primaryLight: '#a8b9ff',
            secondaryColor: '#48bb78',
            secondaryDark: '#38a169',
            secondaryLight: '#9ae6b4',
            successColor: '#48bb78',
            successBg: '#c6f6d5',
            successDark: '#2f855a',
            errorColor: '#e53e3e',
            errorBg: '#fed7d7',
            errorDark: '#c53030',
            warningColor: '#ed8936',
            warningBg: '#ffd89a',
            warningDark: '#c05621',
            infoColor: '#3182ce',
            infoBg: '#bee3f8',
            infoDark: '#2b6cb0',
            borderRadius: 'normal',
            shadowIntensity: 'medium'
        };
    }
    
    applyTheme(theme) {
        const root = document.documentElement;
        
        // Colores primarios
        if (theme.primaryColor) root.style.setProperty('--primary-color', theme.primaryColor);
        if (theme.primaryDark) root.style.setProperty('--primary-dark', theme.primaryDark);
        if (theme.primaryLight) root.style.setProperty('--primary-light', theme.primaryLight);
        
        // Colores secundarios
        if (theme.secondaryColor) root.style.setProperty('--secondary-color', theme.secondaryColor);
        if (theme.secondaryDark) root.style.setProperty('--secondary-dark', theme.secondaryDark);
        if (theme.secondaryLight) root.style.setProperty('--secondary-light', theme.secondaryLight);
        
        // Colores de estado
        if (theme.successColor) root.style.setProperty('--success-color', theme.successColor);
        if (theme.successBg) root.style.setProperty('--success-bg', theme.successBg);
        if (theme.successDark) root.style.setProperty('--success-dark', theme.successDark);
        
        if (theme.errorColor) root.style.setProperty('--error-color', theme.errorColor);
        if (theme.errorBg) root.style.setProperty('--error-bg', theme.errorBg);
        if (theme.errorDark) root.style.setProperty('--error-dark', theme.errorDark);
        
        if (theme.warningColor) root.style.setProperty('--warning-color', theme.warningColor);
        if (theme.warningBg) root.style.setProperty('--warning-bg', theme.warningBg);
        if (theme.warningDark) root.style.setProperty('--warning-dark', theme.warningDark);
        
        if (theme.infoColor) root.style.setProperty('--info-color', theme.infoColor);
        if (theme.infoBg) root.style.setProperty('--info-bg', theme.infoBg);
        if (theme.infoDark) root.style.setProperty('--info-dark', theme.infoDark);
        
        // Bordes
        if (theme.borderRadius) {
            const radiusMap = {
                'sharp': { sm: '4px', md: '6px', lg: '8px', xl: '10px' },
                'normal': { sm: '8px', md: '12px', lg: '15px', xl: '20px' },
                'rounded': { sm: '12px', md: '16px', lg: '20px', xl: '25px' }
            };
            
            const radii = radiusMap[theme.borderRadius] || radiusMap.normal;
            root.style.setProperty('--radius-sm', radii.sm);
            root.style.setProperty('--radius-md', radii.md);
            root.style.setProperty('--radius-lg', radii.lg);
            root.style.setProperty('--radius-xl', radii.xl);
        }
        
        // Sombras
        if (theme.shadowIntensity) {
            const shadowMap = {
                'light': {
                    sm: '0 1px 2px rgba(0,0,0,0.03)',
                    md: '0 2px 8px rgba(0,0,0,0.05)',
                    lg: '0 5px 15px rgba(0,0,0,0.07)',
                    xl: '0 10px 25px rgba(0,0,0,0.1)'
                },
                'medium': {
                    sm: '0 2px 4px rgba(0,0,0,0.05)',
                    md: '0 4px 12px rgba(0,0,0,0.08)',
                    lg: '0 10px 30px rgba(0,0,0,0.1)',
                    xl: '0 20px 40px rgba(0,0,0,0.15)'
                },
                'strong': {
                    sm: '0 3px 6px rgba(0,0,0,0.08)',
                    md: '0 6px 16px rgba(0,0,0,0.12)',
                    lg: '0 12px 35px rgba(0,0,0,0.15)',
                    xl: '0 25px 50px rgba(0,0,0,0.2)'
                }
            };
            
            const shadows = shadowMap[theme.shadowIntensity] || shadowMap.medium;
            root.style.setProperty('--shadow-sm', shadows.sm);
            root.style.setProperty('--shadow-md', shadows.md);
            root.style.setProperty('--shadow-lg', shadows.lg);
            root.style.setProperty('--shadow-xl', shadows.xl);
        }
        
        // Gradiente primario
        root.style.setProperty('--primary-gradient', 
            `linear-gradient(135deg, ${theme.primaryColor || '#667eea'} 0%, ${theme.primaryDark || '#764ba2'} 100%)`
        );
    }
    
    // Método para guardar el tema
    async saveTheme(theme) {
        try {
            const response = await fetch('/api/theme/save/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify(theme)
            });
            
            const result = await response.json();
            if (response.ok && result.success) {
                this.applyTheme(theme); // Aplicar el tema también en el cliente
                return { success: true, theme: result.theme };
            } else {
                throw new Error(result.error || 'Error al guardar tema');
            }
        } catch (error) {
            console.error('Error saving theme:', error);
            return { success: false, error: error.message };
        }
    }
    
    // Método para obtener el tema activo
    async getActiveTheme() {
        try {
            const response = await fetch('/api/theme/active/');
            const result = await response.json();
            
            if (response.ok && result.success) {
                return result.theme;
            } else {
                throw new Error(result.error || 'Error al obtener tema activo');
            }
        } catch (error) {
            console.error('Error getting active theme:', error);
            return null;
        }
    }
    
    // Método para obtener el tema guardado (de localStorage o similar)
    getSavedTheme() {
        try {
            const themeData = document.body.dataset.theme;
            if (themeData) {
                return JSON.parse(themeData);
            }
            return null;
        } catch (e) {
            console.error('Error parsing saved theme:', e);
            return null;
        }
    }
    
    // Método para resetear el tema
    resetTheme() {
        this.applyTheme(this.defaultTheme);
    }
    
    // Método para obtener CSRF token
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Método para obtener temas predefinidos
    getPresetThemes() {
    return {
        // Temas Clásicos
        default: {
            name: 'Predeterminado',
            primaryColor: '#667eea',
            primaryDark: '#764ba2',
            primaryLight: '#a8b9ff',
            secondaryColor: '#48bb78',
            secondaryDark: '#38a169',
            secondaryLight: '#9ae6b4',
            successColor: '#48bb78',
            successBg: '#c6f6d5',
            successDark: '#2f855a',
            errorColor: '#e53e3e',
            errorBg: '#fed7d7',
            errorDark: '#c53030',
            warningColor: '#ed8936',
            warningBg: '#ffd89a',
            warningDark: '#c05621',
            infoColor: '#3182ce',
            infoBg: '#bee3f8',
            infoDark: '#2b6cb0',
            borderRadius: 'normal',
            shadowIntensity: 'medium'
        },
        
        // Temas Sólidos
        azul_solido: {
            name: 'Azul Sólido',
            primaryColor: '#3498db',
            primaryDark: '#2980b9',
            primaryLight: '#5dade2',
            secondaryColor: '#3498db',
            secondaryDark: '#2980b9',
            secondaryLight: '#85c1e9',
            successColor: '#2ecc71',
            successBg: '#d5f5e3',
            successDark: '#27ae60',
            errorColor: '#e74c3c',
            errorBg: '#fadbd8',
            errorDark: '#c0392b',
            warningColor: '#f39c12',
            warningBg: '#fdebd0',
            warningDark: '#d35400',
            infoColor: '#5dade2',
            infoBg: '#d6eaf8',
            infoDark: '#2980b9',
            borderRadius: 'normal',
            shadowIntensity: 'medium'
        },
        
        verde_solido: {
            name: 'Verde Sólido',
            primaryColor: '#2ecc71',
            primaryDark: '#27ae60',
            primaryLight: '#58d68d',
            secondaryColor: '#2ecc71',
            secondaryDark: '#27ae60',
            secondaryLight: '#82e0aa',
            successColor: '#2ecc71',
            successBg: '#d5f5e3',
            successDark: '#27ae60',
            errorColor: '#e74c3c',
            errorBg: '#fadbd8',
            errorDark: '#c0392b',
            warningColor: '#f39c12',
            warningBg: '#fdebd0',
            warningDark: '#d35400',
            infoColor: '#58d68d',
            infoBg: '#d5f5e3',
            infoDark: '#27ae60',
            borderRadius: 'rounded',
            shadowIntensity: 'light'
        },
        
        rojo_solido: {
            name: 'Rojo Sólido',
            primaryColor: '#e74c3c',
            primaryDark: '#c0392b',
            primaryLight: '#f1948a',
            secondaryColor: '#e74c3c',
            secondaryDark: '#c0392b',
            secondaryLight: '#f5b7b1',
            successColor: '#2ecc71',
            successBg: '#d5f5e3',
            successDark: '#27ae60',
            errorColor: '#e74c3c',
            errorBg: '#fadbd8',
            errorDark: '#c0392b',
            warningColor: '#f39c12',
            warningBg: '#fdebd0',
            warningDark: '#d35400',
            infoColor: '#f1948a',
            infoBg: '#fadbd8',
            infoDark: '#c0392b',
            borderRadius: 'sharp',
            shadowIntensity: 'strong'
        },
        
        purpura_solido: {
            name: 'Púrpura Sólido',
            primaryColor: '#9b59b6',
            primaryDark: '#8e44ad',
            primaryLight: '#bb8fce',
            secondaryColor: '#9b59b6',
            secondaryDark: '#8e44ad',
            secondaryLight: '#d2b4de',
            successColor: '#2ecc71',
            successBg: '#d5f5e3',
            successDark: '#27ae60',
            errorColor: '#e74c3c',
            errorBg: '#fadbd8',
            errorDark: '#c0392b',
            warningColor: '#f39c12',
            warningBg: '#fdebd0',
            warningDark: '#d35400',
            infoColor: '#bb8fce',
            infoBg: '#e8daef',
            infoDark: '#8e44ad',
            borderRadius: 'normal',
            shadowIntensity: 'medium'
        },
        
        naranja_solido: {
            name: 'Naranja Sólido',
            primaryColor: '#f39c12',
            primaryDark: '#e67e22',
            primaryLight: '#f8c471',
            secondaryColor: '#f39c12',
            secondaryDark: '#e67e22',
            secondaryLight: '#f9b379',
            successColor: '#2ecc71',
            successBg: '#d5f5e3',
            successDark: '#27ae60',
            errorColor: '#e74c3c',
            errorBg: '#fadbd8',
            errorDark: '#c0392b',
            warningColor: '#f39c12',
            warningBg: '#fdebd0',
            warningDark: '#d35400',
            infoColor: '#f8c471',
            infoBg: '#fdebd0',
            infoDark: '#e67e22',
            borderRadius: 'rounded',
            shadowIntensity: 'light'
        },
        
        // Temas Profesionales
        corporate: {
            name: 'Corporativo',
            primaryColor: '#2c3e50',
            primaryDark: '#1a252f',
            primaryLight: '#34495e',
            secondaryColor: '#3498db',
            secondaryDark: '#2980b9',
            secondaryLight: '#85c1e9',
            successColor: '#27ae60',
            successBg: '#d5f5e3',
            successDark: '#219653',
            errorColor: '#e74c3c',
            errorBg: '#fadbd8',
            errorDark: '#c0392b',
            warningColor: '#f39c12',
            warningBg: '#fdebd0',
            warningDark: '#d35400',
            infoColor: '#3498db',
            infoBg: '#d6eaf8',
            infoDark: '#2980b9',
            borderRadius: 'normal',
            shadowIntensity: 'medium'
        },
        
        moderno: {
            name: 'Moderno',
            primaryColor: '#7f8c8d',
            primaryDark: '#34495e',
            primaryLight: '#bdc3c7',
            secondaryColor: '#95a5a6',
            secondaryDark: '#7f8c8d',
            secondaryLight: '#ecf0f1',
            successColor: '#2ecc71',
            successBg: '#d5f5e3',
            successDark: '#27ae60',
            errorColor: '#e74c3c',
            errorBg: '#fadbd8',
            errorDark: '#c0392b',
            warningColor: '#f39c12',
            warningBg: '#fdebd0',
            warningDark: '#d35400',
            infoColor: '#3498db',
            infoBg: '#d6eaf8',
            infoDark: '#2980b9',
            borderRadius: 'rounded',
            shadowIntensity: 'medium'
        },
        
        // Temas de Modo Oscuro (suaves)
        dark_classic: {
            name: 'Oscuro Clásico',
            primaryColor: '#424242',
            primaryDark: '#212121',
            primaryLight: '#757575',
            secondaryColor: '#616161',
            secondaryDark: '#424242',
            secondaryLight: '#9e9e9e',
            successColor: '#4caf50',
            successBg: '#c8e6c9',
            successDark: '#388e3c',
            errorColor: '#f44336',
            errorBg: '#ffcdd2',
            errorDark: '#d32f2f',
            warningColor: '#ff9800',
            warningBg: '#ffe0b2',
            warningDark: '#f57c00',
            infoColor: '#2196f3',
            infoBg: '#bbdefb',
            infoDark: '#1976d2',
            borderRadius: 'normal',
            shadowIntensity: 'medium'
        },
        
        // Temas Vibrantes
        vibrant: {
            name: 'Vibrante',
            primaryColor: '#ff6b6b',
            primaryDark: '#ee5a52',
            primaryLight: '#ff9e7d',
            secondaryColor: '#4ecdc4',
            secondaryDark: '#2a9d8f',
            secondaryLight: '#88d8b0',
            successColor: '#51cf66',
            successBg: '#d3f9d8',
            successDark: '#37b24d',
            errorColor: '#ff6b6b',
            errorBg: '#ffe3e3',
            errorDark: '#e03131',
            warningColor: '#fcc419',
            warningBg: '#fff3bf',
            warningDark: '#e67700',
            infoColor: '#3bc9db',
            infoBg: '#d0f0fd',
            infoDark: '#1098ad',
            borderRadius: 'rounded',
            shadowIntensity: 'light'
        },
        
        // Temas Pastel
        pastel: {
            name: 'Pastel',
            primaryColor: '#a5d8ff',
            primaryDark: '#74c0fc',
            primaryLight: '#d0ebff',
            secondaryColor: '#ff929f',
            secondaryDark: '#ff6b7f',
            secondaryLight: '#ffe3e6',
            successColor: '#96f2d7',
            successBg: '#e6fcf5',
            successDark: '#40c057',
            errorColor: '#ff8787',
            errorBg: '#ffe3e3',
            errorDark: '#f06565',
            warningColor: '#ffd8a8',
            warningBg: '#fff9db',
            warningDark: '#ff9d00',
            infoColor: '#a5d8ff',
            infoBg: '#e7f5ff',
            infoDark: '#4dabf7',
            borderRadius: 'rounded',
            shadowIntensity: 'light'
        },
        
        // Temas Naturales
        forest: {
            name: 'Bosque',
            primaryColor: '#2d5016',
            primaryDark: '#1e3a0e',
            primaryLight: '#4a7c2d',
            secondaryColor: '#4a7c2d',
            secondaryDark: '#2d5016',
            secondaryLight: '#6b9c4a',
            successColor: '#4a7c2d',
            successBg: '#e8f5e9',
            successDark: '#388e3c',
            errorColor: '#d32f2f',
            errorBg: '#ffebee',
            errorDark: '#b71c1c',
            warningColor: '#f57c00',
            warningBg: '#fff3e0',
            warningDark: '#e65100',
            infoColor: '#1976d2',
            infoBg: '#e3f2fd',
            infoDark: '#0d47a1',
            borderRadius: 'normal',
            shadowIntensity: 'medium'
        },
        
        ocean: {
            name: 'Océano',
            primaryColor: '#006994',
            primaryDark: '#004e70',
            primaryLight: '#0085a1',
            secondaryColor: '#0085a1',
            secondaryDark: '#006994',
            secondaryLight: '#00a8cc',
            successColor: '#00a8cc',
            successBg: '#e0f7fa',
            successDark: '#006994',
            errorColor: '#d32f2f',
            errorBg: '#ffebee',
            errorDark: '#b71c1c',
            warningColor: '#f57c00',
            warningBg: '#fff3e0',
            warningDark: '#e65100',
            infoColor: '#0085a1',
            infoBg: '#e0f7fa',
            infoDark: '#006994',
            borderRadius: 'rounded',
            shadowIntensity: 'medium'
        },
        
        sunset: {
            name: 'Atardecer',
            primaryColor: '#ff6b35',
            primaryDark: '#e55525',
            primaryLight: '#ff9e7d',
            secondaryColor: '#f7931e',
            secondaryDark: '#e07d12',
            secondaryLight: '#ffd8a8',
            successColor: '#40c057',
            successBg: '#d3f9d8',
            successDark: '#2b8a3e',
            errorColor: '#f03e3e',
            errorBg: '#ffe3e3',
            errorDark: '#c92a2a',
            warningColor: '#f59f00',
            warningBg: '#fff3bf',
            warningDark: '#e67700',
            infoColor: '#3bc9db',
            infoBg: '#d0f0fd',
            infoDark: '#1864ab',
            borderRadius: 'sharp',
            shadowIntensity: 'strong'
        },
        
        // Temas Minimalistas
        minimal: {
            name: 'Minimalista',
            primaryColor: '#6c757d',
            primaryDark: '#495057',
            primaryLight: '#adb5bd',
            secondaryColor: '#868e96',
            secondaryDark: '#495057',
            secondaryLight: '#ced4da',
            successColor: '#20c997',
            successBg: '#d1f2eb',
            successDark: '#15967d',
            errorColor: '#e03131',
            errorBg: '#ffdce0',
            errorDark: '#c52222',
            warningColor: '#ffa94d',
            warningBg: '#fff0d9',
            warningDark: '#ff9500',
            infoColor: '#339af0',
            infoBg: '#d0ebff',
            infoDark: '#1c7ed6',
            borderRadius: 'sharp',
            shadowIntensity: 'light'
        },
        
        // Temas de Alta Contraste
        high_contrast: {
            name: 'Alto Contraste',
            primaryColor: '#000000',
            primaryDark: '#000000',
            primaryLight: '#333333',
            secondaryColor: '#ffffff',
            secondaryDark: '#ffffff',
            secondaryLight: '#ffffff',
            successColor: '#00ff00',
            successBg: '#ccffcc',
            successDark: '#00cc00',
            errorColor: '#ff0000',
            errorBg: '#ffcccc',
            errorDark: '#cc0000',
            warningColor: '#ffff00',
            warningBg: '#ffffcc',
            warningDark: '#cccc00',
            infoColor: '#0080ff',
            infoBg: '#cce6ff',
            infoDark: '#0066cc',
            borderRadius: 'sharp',
            shadowIntensity: 'strong'
        }
    };
}
}

// Inicializar solo si no existe
if (typeof window.themeCustomizer === 'undefined') {
    document.addEventListener('DOMContentLoaded', function() {
        window.themeCustomizer = new ThemeCustomizer();
    });
}