from django.urls import path
from . import views

urlpatterns = [
    path('sucursales/', views.lista_sucursales, name='lista_sucursales'),
    path('sucursales/agregar/', views.agregar_sucursal, name='agregar_sucursal'),
    path('sucursales/<int:sucursal_id>/editar/',
         views.editar_sucursal, name='editar_sucursal'),
    path('sucursales/<int:sucursal_id>/eliminar/',
         views.eliminar_sucursal, name='eliminar_sucursal'),
]
