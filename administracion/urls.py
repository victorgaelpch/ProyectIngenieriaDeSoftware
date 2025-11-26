# administracion/urls.py
from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    # Panel principal
    path('administracion', views.panel_admin, name='panel'),
    
    # URLs de Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nueva/', views.CategoriaCreateView.as_view(), name='categoria_add'),
    path('categorias/<uuid:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_edit'),
    path('categorias/<uuid:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    path('categorias/<uuid:categoria_id>/eliminar-ajax/', views.eliminar_categoria, name='categoria_delete_ajax'),
    
    # URLs de Subcategorías
    path('subcategorias/', views.SubcategoriaListView.as_view(), name='subcategoria_list'),
    path('subcategorias/nueva/', views.SubcategoriaCreateView.as_view(), name='subcategoria_add'),
    path('subcategorias/<uuid:pk>/editar/', views.SubcategoriaUpdateView.as_view(), name='subcategoria_edit'),
    path('subcategorias/<uuid:pk>/eliminar/', views.SubcategoriaDeleteView.as_view(), name='subcategoria_delete'),
    path('subcategorias/<uuid:subcategoria_id>/eliminar-ajax/', views.eliminar_subcategoria, name='subcategoria_delete_ajax'),
    
    # URLs de Atributos de Subcategoría
    path('atributos/', views.AtributoSubcategoriaListView.as_view(), name='atributo_list'),
    path('atributos/nuevo/', views.AtributoSubcategoriaCreateView.as_view(), name='atributo_add'),
    path('atributos/<uuid:pk>/editar/', views.AtributoSubcategoriaUpdateView.as_view(), name='atributo_edit'),
    path('atributos/<uuid:pk>/eliminar/', views.AtributoSubcategoriaDeleteView.as_view(), name='atributo_delete'),
    path('atributos/<uuid:atributo_id>/eliminar-ajax/', views.eliminar_atributo, name='atributo_delete_ajax'),
    
    # APIs
    path('api/categorias/<uuid:categoria_id>/subcategorias/', views.get_subcategorias_categoria, name='api_subcategorias_categoria'),
    path('api/subcategorias/<uuid:subcategoria_id>/atributos/', views.get_atributos_subcategoria, name='api_atributos_subcategoria'),
    
    #temas
    path('theme/customizer/', views.theme_customizer, name='theme_customizer'),
    path('api/theme/save/', views.save_theme, name='theme_save'),
    path('api/theme/active/', views.get_active_theme, name='theme_active'),
]