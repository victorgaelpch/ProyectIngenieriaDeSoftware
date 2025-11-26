# caja/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from pedido.models import Pedido, DetallePedido
from pedido.views import sumar_puntos_a_cliente

@staff_member_required
def caja_buscar_pedido(request):
    pedido = None
    mensaje = None
    mensaje_tipo = 'info'
    productos_puntos = []
    
    # Obtener todos los pedidos pendientes para mostrar en la vista
    pedidos_pendientes = Pedido.objects.filter(
        estado__in=['pendiente', 'preparando', 'listo']
    ).order_by('-fecha_hora')[:10]  # Últimos 10 pedidos pendientes
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip().upper()
        nuevo_estado = request.POST.get('nuevo_estado')
        
        if not codigo:
            mensaje = "Por favor ingresa un código de pedido."
            mensaje_tipo = 'warning'
        else:
            try:
                pedido = Pedido.objects.get(codigo=codigo)
                
                if nuevo_estado and nuevo_estado in ['pagado', 'recogido', 'preparando', 'listo']:
                    estado_anterior = pedido.estado
                    
                    # Solo suma puntos si el pedido cambia a 'pagado' y no estaba pagado antes
                    if pedido.estado != 'pagado' and nuevo_estado == 'pagado':
                        if pedido.usuario:
                            try:
                                puntos_ganados = sumar_puntos_a_cliente(pedido.usuario, pedido)
                                pedido.puntos_ganados = puntos_ganados
                                mensaje = f"Estado actualizado a '{nuevo_estado}'. Se otorgaron {puntos_ganados} puntos."
                            except Exception as e:
                                mensaje = f"Estado actualizado a '{nuevo_estado}', pero hubo un error al otorgar puntos: {str(e)}"
                                mensaje_tipo = 'warning'
                        else:
                            mensaje = f"Estado actualizado a '{nuevo_estado}'. No se otorgaron puntos (pedido sin usuario)."
                    else:
                        mensaje = f"Estado actualizado de '{estado_anterior}' a '{nuevo_estado}'."
                    
                    pedido.estado = nuevo_estado
                    pedido.save()
                    mensaje_tipo = 'success'
                    
                    # Recargar pedidos pendientes
                    pedidos_pendientes = Pedido.objects.filter(
                        ESTADOS=['pendiente', 'preparando', 'listo']
                    ).order_by('-fecha_hora')[:10]
                    
                # Cargar detalles del pedido con productos y puntos
                productos_puntos = []
                try:
                    for detalle in pedido.detalles.all():
                        # Obtener puntos extra del producto (con fallback a 0)
                        puntos_extra = getattr(detalle.producto, 'puntos_extra', 0)
                        puntos_totales = puntos_extra * detalle.cantidad
                        
                        productos_puntos.append({
                            'nombre': detalle.producto.nombre,  # ← Corregido de nombre_producto a nombre
                            'cantidad': detalle.cantidad,
                            'subtotal': detalle.subtotal,
                            'puntos_extra_unitario': puntos_extra,
                            'puntos_extra_total': puntos_totales,
                        })
                except Exception as e:
                    print(f"Error al cargar detalles del pedido: {e}")
                    mensaje = f"{mensaje} (Advertencia: No se pudieron cargar todos los detalles del pedido)"
                    mensaje_tipo = 'warning'
                    
            except Pedido.DoesNotExist:
                mensaje = f"No se encontró un pedido con el código '{codigo}'."
                mensaje_tipo = 'error'
            except Exception as e:
                mensaje = f"Error al procesar el pedido: {str(e)}"
                mensaje_tipo = 'error'
                
    elif request.method == 'GET':
        codigo = request.GET.get('codigo', '').strip().upper()
        
        if codigo:
            try:
                pedido = Pedido.objects.get(codigo=codigo)
                
                # Cargar detalles del pedido con productos y puntos
                for detalle in pedido.detalles.all():
                    puntos_extra = getattr(detalle.producto, 'puntos_extra', 0)
                    puntos_totales = puntos_extra * detalle.cantidad
                    
                    productos_puntos.append({
                        'nombre': detalle.producto.nombre,  # ← Corregido
                        'cantidad': detalle.cantidad,
                        'subtotal': detalle.subtotal,
                        'puntos_extra_unitario': puntos_extra,
                        'puntos_extra_total': puntos_totales,
                    })
                    
            except Pedido.DoesNotExist:
                mensaje = f"No se encontró un pedido con el código '{codigo}'."
                mensaje_tipo = 'error'
            except Exception as e:
                mensaje = f"Error al buscar el pedido: {str(e)}"
                mensaje_tipo = 'error'
    
    # Calcular totales de puntos
    total_puntos_productos = sum(p['puntos_extra_total'] for p in productos_puntos)
    puntos_por_compra = int(pedido.total // 30) * 5 if pedido else 0
    total_puntos = total_puntos_productos + puntos_por_compra
    
    return render(request, 'caja/caja_buscar_pedido.html', {
        'pedido': pedido,
        'mensaje': mensaje,
        'mensaje_tipo': mensaje_tipo,
        'productos_puntos': productos_puntos,
        'pedidos_pendientes': pedidos_pendientes,
        'total_puntos_productos': total_puntos_productos,
        'puntos_por_compra': puntos_por_compra,
        'total_puntos': total_puntos,
    })


@staff_member_required
def eliminar_pedido(request, pedido_id):
    """Eliminar un pedido"""
    try:
        pedido = get_object_or_404(Pedido, id=pedido_id)
        codigo = pedido.codigo
        pedido.delete()
        messages.success(request, f'Pedido {codigo} eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar el pedido: {str(e)}')
    
    return redirect('caja:lista_pedidos_caja')


# caja/views.py - Agregar/actualizar estas vistas

@staff_member_required
def lista_pedidos_caja(request):
    """Vista para listar todos los pedidos en caja con filtros"""
    estado_filtro = request.GET.get('estado', 'todos')
    fecha_filtro = request.GET.get('fecha', 'todos')
    buscar = request.GET.get('buscar', '').strip()
    
    # Filtro base
    pedidos = Pedido.objects.all()
    
    # Filtro por estado
    if estado_filtro != 'todos':
        pedidos = pedidos.filter(estado=estado_filtro)
    
    # Filtro por fecha
    from django.utils import timezone
    from datetime import timedelta
    
    hoy = timezone.now().date()
    if fecha_filtro == 'hoy':
        pedidos = pedidos.filter(fecha_hora__date=hoy)
    elif fecha_filtro == 'ayer':
        ayer = hoy - timedelta(days=1)
        pedidos = pedidos.filter(fecha_hora__date=ayer)
    elif fecha_filtro == 'semana':
        inicio_semana = hoy - timedelta(days=7)
        pedidos = pedidos.filter(fecha_hora__date__gte=inicio_semana)
    elif fecha_filtro == 'mes':
        inicio_mes = hoy - timedelta(days=30)
        pedidos = pedidos.filter(fecha_hora__date__gte=inicio_mes)
    
    # Búsqueda por código o usuario
    if buscar:
        pedidos = [p for p in pedidos if buscar.upper() in p.codigo.upper() or 
                   (p.usuario and buscar.lower() in p.usuario.username.lower())]
    
    # Ordenar por fecha más reciente
    pedidos = sorted(pedidos, key=lambda x: x.fecha_hora, reverse=True)
    
    # Estadísticas
    todos_pedidos = list(Pedido.objects.all())
    estadisticas = {
        'total': len(todos_pedidos),
        'pendientes': len([p for p in todos_pedidos if p.estado == 'pendiente']),
        'preparando': len([p for p in todos_pedidos if p.estado == 'preparando']),
        'listos': len([p for p in todos_pedidos if p.estado == 'listo']),
        'pagados': len([p for p in todos_pedidos if p.estado == 'pagado']),
        'recogidos': len([p for p in todos_pedidos if p.estado == 'recogido']),
        'cancelados': len([p for p in todos_pedidos if p.estado == 'cancelado']),
    }
    
    # Calcular totales del día
    pedidos_hoy = [p for p in todos_pedidos if p.fecha_hora.date() == hoy]
    total_ventas_hoy = sum(float(p.total) for p in pedidos_hoy if p.estado in ['pagado', 'recogido'])
    
    return render(request, 'caja/lista_pedidos.html', {
        'pedidos': pedidos,
        'estado_filtro': estado_filtro,
        'fecha_filtro': fecha_filtro,
        'buscar': buscar,
        'estadisticas': estadisticas,
        'total_ventas_hoy': total_ventas_hoy,
    })


@staff_member_required
def detalle_pedido_caja(request, pedido_id):
    """Vista detallada de un pedido desde caja"""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    mensaje = None
    mensaje_tipo = 'info'
    productos_puntos = []

    # Si se envía un cambio de estado por POST
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')

        if nuevo_estado and nuevo_estado in ['pagado', 'recogido', 'preparando', 'listo', 'cancelado']:
            estado_anterior = pedido.estado

            # Solo suma puntos si el pedido cambia a 'pagado' y no estaba pagado antes
            if pedido.estado != 'pagado' and nuevo_estado == 'pagado':
                if pedido.usuario:
                    try:
                        puntos_ganados = sumar_puntos_a_cliente(pedido.usuario, pedido)
                        pedido.puntos_ganados = puntos_ganados
                        mensaje = f"Estado actualizado a '{nuevo_estado}'. Se otorgaron {puntos_ganados} puntos."
                    except Exception as e:
                        mensaje = f"Estado actualizado a '{nuevo_estado}', pero hubo un error al otorgar puntos: {str(e)}"
                        mensaje_tipo = 'warning'
                else:
                    mensaje = f"Estado actualizado a '{nuevo_estado}'. No se otorgaron puntos (pedido sin usuario)."
            else:
                mensaje = f"Estado actualizado de '{estado_anterior}' a '{nuevo_estado}'."

            pedido.estado = nuevo_estado
            pedido.save()
            mensaje_tipo = 'success'

    # Cargar detalles del pedido con productos y puntos
    for detalle in pedido.detalles.all():
        puntos_extra = getattr(detalle, 'puntos_extra', 0)  # usar campo cacheado si lo agregaste
        puntos_totales = puntos_extra * detalle.cantidad

        productos_puntos.append({
            'nombre': detalle.nombre_producto,
            'cantidad': detalle.cantidad,
            'subtotal': detalle.subtotal,
            'precio_unitario': detalle.precio_unitario,
            'puntos_extra_unitario': puntos_extra,
            'puntos_extra_total': puntos_totales,
        })

    # Calcular totales de puntos
    total_puntos_productos = sum(p['puntos_extra_total'] for p in productos_puntos)
    puntos_por_compra = int(pedido.total // 30) * 5 if pedido else 0
    total_puntos = total_puntos_productos + puntos_por_compra

    return render(request, 'caja/detalle_pedido.html', {
        'pedido': pedido,
        'mensaje': mensaje,
        'mensaje_tipo': mensaje_tipo,
        'productos_puntos': productos_puntos,
        'total_puntos_productos': total_puntos_productos,
        'puntos_por_compra': puntos_por_compra,
        'total_puntos': total_puntos,
    })




@staff_member_required
def cambiar_estado_pedido(request, pedido_id):
    """Cambiar estado de un pedido desde la lista"""
    if request.method == 'POST':
        try:
            pedido = get_object_or_404(Pedido, id=pedido_id)
            nuevo_estado = request.POST.get('nuevo_estado')
            
            if nuevo_estado in ['pendiente', 'preparando', 'listo', 'pagado', 'recogido', 'cancelado']:
                estado_anterior = pedido.estado
                
                # Solo suma puntos si cambia a 'pagado' y no estaba pagado antes
                if pedido.estado != 'pagado' and nuevo_estado == 'pagado':
                    if pedido.usuario:
                        try:
                            puntos_ganados = sumar_puntos_a_cliente(pedido.usuario, pedido)
                            pedido.puntos_ganados = puntos_ganados
                            messages.success(request, f'Pedido {pedido.codigo} marcado como pagado. Se otorgaron {puntos_ganados} puntos.')
                        except Exception as e:
                            messages.warning(request, f'Pedido actualizado pero error al otorgar puntos: {str(e)}')
                    else:
                        messages.success(request, f'Pedido {pedido.codigo} marcado como pagado (sin usuario).')
                else:
                    messages.success(request, f'Estado del pedido {pedido.codigo} actualizado de "{estado_anterior}" a "{nuevo_estado}".')
                
                pedido.estado = nuevo_estado
                pedido.save()
            else:
                messages.error(request, 'Estado no válido.')
                
        except Exception as e:
            messages.error(request, f'Error al actualizar el pedido: {str(e)}')
    
    return redirect('caja:lista_pedidos_caja')


@staff_member_required
def imprimir_ticket(request, pedido_id):
    """Vista para imprimir ticket del pedido"""
    try:
        pedido = get_object_or_404(Pedido, id=pedido_id)

        # Obtener detalles
        productos_detalle = []
        for detalle in pedido.detalles.all():
            productos_detalle.append({
                'nombre': detalle.nombre_producto,  
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario, 
                'subtotal': detalle.subtotal,
            })
        print(productos_detalle)
        return render(request, 'caja/ticket_imprimir.html', {
            'pedido': pedido,
            'productos_detalle': productos_detalle,
        })

    except Exception as e:
        messages.error(request, f'Error al generar ticket: {str(e)}')
        return redirect('caja:lista_pedidos_caja')

