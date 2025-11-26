from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/editar/<int:direccion_id>/eliminar/',
         views.eliminar_direccion, name='eliminar_direccion'),
    path('perfil/editar/<int:direccion_id>/editar/',
         views.editar_direccion, name='editar_direccion'),
]
