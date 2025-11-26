# menu/urls.py
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('productos/', views.lista_productos, name='producto_list'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/<uuid:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<uuid:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
]