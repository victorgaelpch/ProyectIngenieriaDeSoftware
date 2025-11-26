// theme-customizer.js
class ThemeCustomizer {
    constructor() {
        this.defaultTheme = {
            primaryColor: '#667eea',
            primaryDark: '#764ba2',
            secondaryColor: '#48bb78',
            borderRadius: 'normal',
            shadowIntensity: 'medium'
        };
        
        this.loadTheme();
    }
    
    loadTheme() {
        const savedTheme = this.getSavedTheme();
        if (savedTheme) {
            this.applyTheme(savedTheme);
        }
    }
    
    getSavedTheme() {
        const themeData = document.body.dataset.theme;
        if (themeData) {
            try {
                return JSON.parse(themeData);
            } catch (e) {
                console.error('Error parsing theme data:', e);
                return null;
            }
        }
        return null;
    }
    
    applyTheme(theme) {
        const root = document.documentElement;
        
        if (theme.primaryColor) {
            root.style.setProperty('--primary-color', theme.primaryColor);
        }
        
        if (theme.primaryDark) {
            root.style.setProperty('--primary-dark', theme.primaryDark);
        }
        
        if (theme.secondaryColor) {
            root.style.setProperty('--secondary-color', theme.secondaryColor);
            root.style.setProperty('--success-color', theme.secondaryColor);
        }
        
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
        
     
        root.style.setProperty('--primary-gradient', 
            `linear-gradient(135deg, ${theme.primaryColor || '#667eea'} 0%, ${theme.primaryDark || '#764ba2'} 100%)`
        );
    }
    
    async saveTheme(theme) {
        try {
            const response = await fetch('/administracion/api/theme/save/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify(theme)
            });
            
            if (response.ok) {
                this.applyTheme(theme);
                return { success: true };
            } else {
                throw new Error('Error al guardar tema');
            }
        } catch (error) {
            console.error('Error saving theme:', error);
            return { success: false, error: error.message };
        }
    }
    
    resetTheme() {
        this.applyTheme(this.defaultTheme);
    }
    
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
    
    getPresetThemes() {
        return {
            default: {
                name: 'Predeterminado',
                primaryColor: '#667eea',
                primaryDark: '#764ba2',
                secondaryColor: '#48bb78',
                borderRadius: 'normal',
                shadowIntensity: 'medium'
            },
            amanecer: {
                name: 'Amanecer',
                primaryColor: '#FF5F6D',
                primaryDark: '#FFC371',
                secondaryColor: '#FFD700',
                borderRadius: 'rounded',
                shadowIntensity: 'light'
            },
            oceano: {
                name: 'Océano',
                primaryColor: '#00C9FF',
                primaryDark: '#92FE9D',
                secondaryColor: '#48BB78',
                borderRadius: 'normal',
                shadowIntensity: 'medium'
            },
            atardecer: {
                name: 'Atardecer',
                primaryColor: '#667eea',
                primaryDark: '#764ba2',
                secondaryColor: '#f6d365',
                borderRadius: 'sharp',
                shadowIntensity: 'strong'
            },
            bosque: {
                name: 'Bosque',
                primaryColor: '#11998e',
                primaryDark: '#38ef7d',
                secondaryColor: '#80ed99',
                borderRadius: 'rounded',
                shadowIntensity: 'medium'
            },
            fuego: {
                name: 'Fuego',
                primaryColor: '#f12711',
                primaryDark: '#f5af19',
                secondaryColor: '#fbc531',
                borderRadius: 'normal',
                shadowIntensity: 'strong'
            }
        };
    }
}

document.addEventListener('DOMContentLoaded', function() {
    window.themeCustomizer = new ThemeCustomizer();
});

if (document.readyState === 'complete' || document.readyState === 'interactive') {
    window.themeCustomizer = new ThemeCustomizer();
}