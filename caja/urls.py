from django.urls import path
from . import views

app_name = 'caja'

# caja/urls.py

urlpatterns = [
    path('', views.caja_buscar_pedido, name='caja_buscar_pedido'),
    path('pedidos/', views.lista_pedidos_caja, name='lista_pedidos_caja'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido_caja, name='detalle_pedido_caja'),
    path('pedidos/<int:pedido_id>/cambiar-estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pedidos/<int:pedido_id>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),
    path('pedidos/<int:pedido_id>/ticket/', views.imprimir_ticket, name='imprimir_ticket'),
]
