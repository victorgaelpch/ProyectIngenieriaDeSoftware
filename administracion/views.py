from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from menu.models import Categoria, Subcategoria, AtributoSubcategoria
from .forms import CategoriaForm, SubcategoriaForm, AtributoSubcategoriaForm
import uuid
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .models import SiteTheme

def es_gerente(user):
    return user.is_authenticated and user.groups.filter(name='Gerente').exists()


def panel_admin(request):
    #guardamos el en cache para las estadisticas del panel
    cache_key = 'panel_stats'
    context = cache.get(cache_key)
    
    if not context:
        # Si no esta en cache, calcular
        categorias_list = list(Categoria.objects.all())
        subcategorias_list = list(Subcategoria.objects.all())
        atributos_list = list(AtributoSubcategoria.objects.all())
        
        context = {
            'total_categorias': len(categorias_list),
            'categorias_activas': len([c for c in categorias_list if c.activo]),
            'total_subcategorias': len(subcategorias_list),
            'subcategorias_activas': len([s for s in subcategorias_list if s.activo]),
            'total_atributos': len(atributos_list),
            'atributos_requeridos': len([a for a in atributos_list if a.requerido]),
        }
        
        try:
            from menu.models import Producto
            productos_list = list(Producto.objects.all())
            context.update({
                'total_productos': len(productos_list),
                'productos_activos': len([p for p in productos_list if p.activo]),
            })
        except ImportError:
            context.update({
                'total_productos': 0,
                'productos_activos': 0,
            })
        
        # Guardar en cache por 30 segundos
        cache.set(cache_key, context, 30)
    
    return render(request, 'administracion/panel.html', context)

def panel_aadmin(request):
    context = {
        'total_categorias': Categoria.objects.count(),
        'categorias_activas': Categoria.objects.filter(activo=True).count(),
        'total_subcategorias': Subcategoria.objects.count(), 
        'subcategorias_activas': Subcategoria.objects.filter(activo=True).count(),
        'total_atributos': AtributoSubcategoria.objects.count(),
        'atributos_requeridos': AtributoSubcategoria.objects.filter(requerido=True).count(),
    }
   
    return render(request, 'administracion/panel.html',context)

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'administracion/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'administracion/categoria_form.html'
    success_url = reverse_lazy('administracion:categoria_list')
    
    def form_valid(self, form):
        cache.delete('panel_stats')
        messages.success(self.request, 'Categoría creada exitosamente.')
        print(f'Categoriaaaaaa:{Categoria.objects.count()}')
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'administracion/categoria_form.html'
    success_url = reverse_lazy('administracion:categoria_list')
    
    def form_valid(self, form):
        cache.delete('panel_stats')
        messages.success(self.request, 'Categoría actualizada exitosamente.')
        return super().form_valid(form)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    success_url = reverse_lazy('administracion:categoria_list')
    
    def delete(self, request, *args, **kwargs):
        cache.delete('panel_stats')
        messages.success(self.request, 'Categoría eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

def eliminar_categoria(request, categoria_id):
    if request.method == 'POST':
        try:
            categoria = get_object_or_404(Categoria, id=categoria_id)
            categoria.delete()
            return JsonResponse({'success': True, 'message': 'Categoría eliminada exitosamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

class SubcategoriaListView(LoginRequiredMixin, ListView):
    model = Subcategoria
    template_name = 'administracion/subcategoria_list.html'
    context_object_name = 'subcategorias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias=Categoria.objects.all()
        
        categorias_dict={cat.id:cat.nombre for cat in categorias}
        
        subcategorias=list(context['subcategorias'])
        for subcat in subcategorias:
            subcat.categoria_nombre=categorias_dict[subcat.categoria_id]
            #print(f'categorias_dict: {categorias_dict[subcat.categoria_id]}')
            #print(f'subcategoria: {subcat.categoria_nombre} - {categorias_dict.get(str(subcat.categoria_id))} - {subcat.categoria_id}')
        context['subcategorias']=subcategorias
        
        return context

class SubcategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Subcategoria
    form_class = SubcategoriaForm
    template_name = 'administracion/subcategoria_form.html'
    success_url = reverse_lazy('administracion:subcategoria_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subcategoría creada exitosamente.')
        return super().form_valid(form)

class SubcategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Subcategoria
    form_class = SubcategoriaForm
    template_name = 'administracion/subcategoria_form.html'
    success_url = reverse_lazy('administracion:subcategoria_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subcategoría actualizada exitosamente.')
        return super().form_valid(form)

class SubcategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Subcategoria
    success_url = reverse_lazy('administracion:subcategoria_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Subcategoría eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

def eliminar_subcategoria(request, subcategoria_id):
    if request.method == 'POST':
        try:
            subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
            subcategoria.delete()
            return JsonResponse({'success': True, 'message': 'Subcategoría eliminada exitosamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

class AtributoSubcategoriaListView(LoginRequiredMixin, ListView):
    model = AtributoSubcategoria
    template_name = 'administracion/atributo_list.html'
    context_object_name = 'atributos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar nombres de subcategorias y categorías
        subcategorias_dict = {}
        categorias_dict = {}
        
        # Primero obtener categorías
        categorias = Categoria.objects.all()
        categorias_dict={cat.id: cat.nombre for cat in categorias}
        
        # Luego subcategorías
        subcategorias = Subcategoria.objects.all()
        subcategorias_dict = {
            str(sub.id): {
                "nombre": sub.nombre,
                "categoria_nombre": categorias_dict[sub.categoria_id]
            }
            for sub in subcategorias
        }
        
        # Agregar información a cada atributo
        atributos = list(context["atributos"])
        for atributo in atributos:
            sub_info = subcategorias_dict.get(
                str(atributo.subcategoria_id),
                {"nombre": "Sin subcategoría", "categoria_nombre": "Sin categoría"}
            )
            atributo.subcategoria_nombre = sub_info["nombre"]
            atributo.categoria_nombre = sub_info["categoria_nombre"]
            print(f'atributo: {atributo.nombre}, subcategoria: {atributo.subcategoria_nombre}, categoria: {atributo.categoria_nombre}')
        
        context["atributos"] = atributos
        return context

class AtributoSubcategoriaCreateView(LoginRequiredMixin, CreateView):
    model = AtributoSubcategoria
    form_class = AtributoSubcategoriaForm
    template_name = 'administracion/atributo_form.html'
    success_url = reverse_lazy('administracion:atributo_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Atributo creado exitosamente.')
        return super().form_valid(form)

class AtributoSubcategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = AtributoSubcategoria
    form_class = AtributoSubcategoriaForm
    template_name = 'administracion/atributo_form.html'
    success_url = reverse_lazy('administracion:atributo_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Atributo actualizado exitosamente.')
        return super().form_valid(form)

class AtributoSubcategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = AtributoSubcategoria
    success_url = reverse_lazy('administracion:atributo_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Atributo eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

def eliminar_atributo(request, atributo_id):
    if request.method == 'POST':
        try:
            atributo = get_object_or_404(AtributoSubcategoria, id=atributo_id)
            atributo.delete()
            return JsonResponse({'success': True, 'message': 'Atributo eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

# API
@user_passes_test(es_gerente)
def get_subcategorias_categoria(request, categoria_id):
    """Obtener subcategorías de una categoría específica"""
    es_gerente_flag = es_gerente(request.user)
    if not es_gerente_flag:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id, activo=True)
    
    return JsonResponse({
        'subcategorias': [
            {
                'id': str(subcat.id),
                'nombre': subcat.nombre,
                'descripcion': subcat.descripcion or ''
            } for subcat in subcategorias
        ]
    })
@user_passes_test(es_gerente)
def get_atributos_subcategoria(request, subcategoria_id):
    """Obtener atributos de una subcategoría específica"""
    es_gerente_flag = es_gerente(request.user)
    if not es_gerente_flag:
        return JsonResponse({'error': 'No autorizado'}, status=403)
        
    atributos = AtributoSubcategoria.objects.filter(subcategoria_id=subcategoria_id)
    return JsonResponse({
        'atributos': [
            {
                'id': str(attr.id),
                'nombre': attr.nombre,
                'tipo': attr.tipo,
                'requerido': attr.requerido,
                'opciones': attr.opciones or []
            } for attr in atributos
        ]
    })
    
def theme_customizer(request):
    """Vista para el personalizador de temas"""

    active_theme = SiteTheme.get_active_theme()
    
    context = {
        'active_theme': active_theme,
        'theme_json': active_theme.to_json() if active_theme else '{}'
    }
    
    return render(request, 'administracion/theme_customizer.html', context)

@require_http_methods(["POST"])
@require_http_methods(["POST"])
def save_theme(request):
    """Guardar configuración del tema"""
    try:
        data = json.loads(request.body)
        
        # Función para limpiar el valor hexadecimal
        def clean_hex_color(value, default):
            if not value:
                return default
            # Eliminar el '#' si está presente y tomar solo los primeros 6 caracteres
            cleaned = value.lstrip('#')[:6]
            # Validar que sea un color hexadecimal válido
            if len(cleaned) != 6 or not all(c in '0123456789ABCDEFabcdef' for c in cleaned):
                return default
            return cleaned

        # Limpiar los colores (ahora con el formato correcto para el modelo)
        primary_color = clean_hex_color(data.get('primaryColor'), '667eea')
        primary_dark = clean_hex_color(data.get('primaryDark'), '764ba2')
        primary_light = clean_hex_color(data.get('primaryLight'), 'a8b9ff')
        
        secondary_color = clean_hex_color(data.get('secondaryColor'), '48bb78')
        secondary_dark = clean_hex_color(data.get('secondaryDark'), '38a169')
        secondary_light = clean_hex_color(data.get('secondaryLight'), '9ae6b4')
        
        success_color = clean_hex_color(data.get('successColor'), '48bb78')
        success_bg = clean_hex_color(data.get('successBg'), 'c6f6d5')
        success_dark = clean_hex_color(data.get('successDark'), '2f855a')
        
        error_color = clean_hex_color(data.get('errorColor'), 'e53e3e')
        error_bg = clean_hex_color(data.get('errorBg'), 'fed7d7')
        error_dark = clean_hex_color(data.get('errorDark'), 'c53030')
        
        warning_color = clean_hex_color(data.get('warningColor'), 'ed8936')
        warning_bg = clean_hex_color(data.get('warningBg'), 'ffd89a')
        warning_dark = clean_hex_color(data.get('warningDark'), 'c05621')
        
        info_color = clean_hex_color(data.get('infoColor'), '3182ce')
        info_bg = clean_hex_color(data.get('infoBg'), 'bee3f8')
        info_dark = clean_hex_color(data.get('infoDark'), '2b6cb0')

        # Validar otros campos
        border_radius = data.get('borderRadius', 'normal')
        shadow_intensity = data.get('shadowIntensity', 'medium')

        # Validar opciones permitidas
        allowed_border_radius = ['sharp', 'normal', 'rounded']
        allowed_shadow_intensity = ['light', 'medium', 'strong']

        if border_radius not in allowed_border_radius:
            border_radius = 'normal'
        if shadow_intensity not in allowed_shadow_intensity:
            shadow_intensity = 'medium'

        # Desactivar todos los temas
        SiteTheme.objects.update(is_active=False)
        
        # Crear o actualizar el tema
        theme, created = SiteTheme.objects.get_or_create(
            name='custom',
            defaults={
                'primary_color': primary_color.upper(),
                'primary_dark': primary_dark.upper(),
                'primary_light': primary_light.upper(),
                'secondary_color': secondary_color.upper(),
                'secondary_dark': secondary_dark.upper(),
                'secondary_light': secondary_light.upper(),
                'success_color': success_color.upper(),
                'success_bg': success_bg.upper(),
                'success_dark': success_dark.upper(),
                'error_color': error_color.upper(),
                'error_bg': error_bg.upper(),
                'error_dark': error_dark.upper(),
                'warning_color': warning_color.upper(),
                'warning_bg': warning_bg.upper(),
                'warning_dark': warning_dark.upper(),
                'info_color': info_color.upper(),
                'info_bg': info_bg.upper(),
                'info_dark': info_dark.upper(),
                'border_radius': border_radius,
                'shadow_intensity': shadow_intensity,
                'is_active': True
            }
        )
        
        if not created:
            theme.primary_color = primary_color.upper()
            theme.primary_dark = primary_dark.upper()
            theme.primary_light = primary_light.upper()
            theme.secondary_color = secondary_color.upper()
            theme.secondary_dark = secondary_dark.upper()
            theme.secondary_light = secondary_light.upper()
            theme.success_color = success_color.upper()
            theme.success_bg = success_bg.upper()
            theme.success_dark = success_dark.upper()
            theme.error_color = error_color.upper()
            theme.error_bg = error_bg.upper()
            theme.error_dark = error_dark.upper()
            theme.warning_color = warning_color.upper()
            theme.warning_bg = warning_bg.upper()
            theme.warning_dark = warning_dark.upper()
            theme.info_color = info_color.upper()
            theme.info_bg = info_bg.upper()
            theme.info_dark = info_dark.upper()
            theme.border_radius = border_radius
            theme.shadow_intensity = shadow_intensity
            theme.is_active = True
            theme.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Tema guardado exitosamente',
            'theme': theme.to_dict()
        })
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return JsonResponse({
            'success': False,
            'error': f'Datos JSON inválidos: {str(e)}'
        }, status=400)
    except Exception as e:
        print(f"Error al guardar el tema: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': f'Error interno al guardar el tema: {str(e)}'
        }, status=500)
        
@require_http_methods(["GET"])
def get_active_theme(request):
    """Obtener el tema activo (público)"""
    theme = SiteTheme.get_active_theme()
    
    if theme:
        return JsonResponse({
            'success': True,
            'theme': theme.to_dict()
        })
    else:
        return JsonResponse({
            'success': True,
            'theme': None
        })
        

