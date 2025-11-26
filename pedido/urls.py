from django.urls import path
from . import views

urlpatterns = [
    path('ordenar/', views.seleccionar_tipo_pedido,
         name='seleccionar_tipo_pedido'),
    path('ordenar/pickup/', views.pickup_pedido, name='pickup_pedido'),
    path('pedidos/pickup/', views.lista_pedidos_pickup,
         name='lista_pedidos_pickup'),
    path('pedidos/pickup/<int:pedido_id>/',
         views.detalle_pedido_pickup, name='detalle_pedido_pickup'),
    path('ordenar/kiosko/', views.kiosko_pedido, name='kiosko_pedido'),
    path('pedidos/cancelar/<int:pedido_id>/',
         views.cancelar_pedido, name='cancelar_pedido'),
    path('pedidos/estado/<int:pedido_id>/',
         views.pickup_exito_estado, name='pickup_exito_estado'),
    path('puntos/', views.puntos_recompensas, name='puntos_recompensas'),
]
