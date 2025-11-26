from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sucursal, Pedido, PedidoPickup, DetallePedido
from .forms import PedidoPickupForm
from menu.models import Producto, Categoria
import json
from django.utils import timezone
from decimal import Decimal


def seleccionar_tipo_pedido(request):
    return render(request, 'pedido/tipo_pedido.html')


@login_required
def pickup_pedido(request):
    nombre = request.user.get_full_name() or ''
    correo = request.user.email or ''
    telefono = ''
    perfil = getattr(request.user, 'perfil', None)
    if perfil:
        telefono = perfil.telefono or ''

    sucursales = Sucursal.objects.all()
    productos = Producto.objects.filter(activo=True)  # Solo productos activos
    form = PedidoPickupForm()

    VALOR_PUNTO = Decimal('0.50')

    if request.method == 'POST':
        form = PedidoPickupForm(request.POST)
        tipo_pago = request.POST.get('tipo_pago')
        nombre_post = request.POST.get('nombre')
        correo_post = request.POST.get('correo')
        telefono_post = request.POST.get('telefono')
        carrito_json = request.POST.get('carrito_json')
        carrito = json.loads(carrito_json) if carrito_json else []

        # Validación para pago en efectivo
        if tipo_pago == 'efectivo':
            if not nombre_post or not correo_post or not telefono_post:
                messages.error(request, "Debes completar todos los datos para pago en efectivo.")
                return render(request, 'pedido/pickup.html', {
                    'sucursales': sucursales,
                    'form': form,
                    'productos': productos,
                    'categorias': Categoria.objects.filter(activo=True),
                    'nombre': nombre_post,
                    'correo': correo_post,
                    'telefono': telefono_post,
                })

        if form.is_valid():
            horario_recoleccion = form.cleaned_data['horario_recoleccion']
            sucursal_id = request.POST.get('sucursal')
            sucursal = Sucursal.objects.get(id=sucursal_id)

            # Calcular total del carrito
            total = Decimal('0.00')
            for item in carrito:
                producto = Producto.objects.get(id=item['id'])
                cantidad = int(item['cantidad'])
                subtotal = producto.precio * cantidad
                total += subtotal

            # Pago con puntos
            puntos_a_usar = int(request.POST.get('puntos_a_usar', 0))
            max_puntos = min(perfil.puntos if perfil else 0, int(total // VALOR_PUNTO))
            puntos_a_usar = min(puntos_a_usar, max_puntos)
            total_final = total - (puntos_a_usar * VALOR_PUNTO)

            estado_pedido = 'pagado' if total_final == 0 else 'pendiente'

            # Crear pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                sucursal=sucursal,
                estado=estado_pedido,
                total=total_final,
                puntos_usados=puntos_a_usar,
            )

            # Crear detalles del pedido
            for item in carrito:
                producto = Producto.objects.get(id=item['id'])
                cantidad = int(item['cantidad'])
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto_id=producto.id,  # ✅ usar producto_id (UUID)
                    cantidad=cantidad,
                )

            # Restar puntos usados
            if perfil and puntos_a_usar > 0:
                perfil.puntos -= puntos_a_usar
                perfil.save()

            # Crear registro de pickup
            PedidoPickup.objects.create(
                pedido=pedido,
                horario_recoleccion=horario_recoleccion,
                tipo_pago=tipo_pago,
            )

            # Actualizar datos del usuario si es pago en efectivo
            user = request.user
            if tipo_pago == 'efectivo':
                if not user.first_name and nombre_post:
                    user.first_name = nombre_post.split()[0]
                    if len(nombre_post.split()) > 1:
                        user.last_name = " ".join(nombre_post.split()[1:])
                if not user.email and correo_post:
                    user.email = correo_post
                user.save()
                if perfil and not perfil.telefono and telefono_post:
                    perfil.telefono = telefono_post
                    perfil.save()

            return redirect('pickup_exito_estado', pedido_id=pedido.id)

    categorias = Categoria.objects.filter(activo=True)

    return render(request, 'pedido/pickup.html', {
        'sucursales': sucursales,
        'form': form,
        'productos': productos,
        'categorias': categorias,
        'nombre': nombre,
        'correo': correo,
        'telefono': telefono,
        'perfil': perfil,
    })




@login_required
def pickup_exito_estado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'pedido/pickup_exito.html', {
        'pedido': pedido,
        'sucursal': pedido.sucursal,
        'horario': pedido.pickup.horario_recoleccion,
    })


@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    if pedido.estado == 'pendiente':
        pedido.estado = 'cancelado'
        pedido.save()
    return redirect('lista_pedidos_pickup')


@login_required
def detalle_pedido_pickup(request, pedido_id):
    pedido = Pedido.objects.select_related('sucursal', 'pickup').get(id=pedido_id)
    detalles = pedido.detalles.all()  # ya tienes los detalles
    return render(request, 'pedido/detalle_pedido_pickup.html', {
        'pedido': pedido,
        'detalles': detalles,
    })



@login_required
def lista_pedidos_pickup(request):
    mostrar_recogidos = request.GET.get('mostrar_recogidos') == '1'
    mostrar_cancelados = request.GET.get('mostrar_cancelados') == '1'

    estados = ['pendiente', 'preparando','listo', 'pagado']
    if mostrar_recogidos:
        estados.append('recogido')
    if mostrar_cancelados:
        estados.append('cancelado')
    pedidos = Pedido.objects.filter(
        pickup__isnull=False,
        estado__in=estados,
        usuario=request.user
    ).select_related('sucursal', 'pickup').order_by('pickup__horario_recoleccion')

    return render(request, 'pedido/lista_pedidos_pickup.html', {
        'pedidos': pedidos,
        'mostrar_recogidos': mostrar_recogidos,
        'mostrar_cancelados': mostrar_cancelados,
    })


def sumar_puntos_a_cliente(usuario, pedido):
    if not usuario or not hasattr(usuario, 'perfil'):
        return 0
    perfil = usuario.perfil

    # puntos por monto gastado
    puntos_por_total = int(pedido.total // 30) * 5

    # puntos extra por producto
    puntos_extra = 0
    from menu.models import Producto
    for detalle in pedido.detalles.all():
        try:
            producto = Producto.objects.get(id=detalle.producto_id)
            puntos_extra += producto.puntos_extra * detalle.cantidad
        except Producto.DoesNotExist:
            pass

    total_puntos = puntos_por_total + puntos_extra
    perfil.puntos += total_puntos
    perfil.save()
    return total_puntos



def usar_puntos_en_pedido(usuario, pedido):
    perfil = usuario.perfil

    puntos_a_usar = min(perfil.puntos, int(pedido.total))
    pedido.total -= puntos_a_usar
    perfil.puntos -= puntos_a_usar
    perfil.save()
    pedido.save()
    return puntos_a_usar

@login_required
def puntos_recompensas(request):
    perfil = request.user.perfil
    pedidos = Pedido.objects.filter(
        usuario=request.user, estado='pagado'
    ).order_by('-fecha_hora')
    pedidos_con_detalles = []
    from menu.models import Producto
    for pedido in pedidos:
        detalles = []
        for detalle in pedido.detalles.all():
            puntos_extra = 0
            try:
                producto = Producto.objects.get(id=detalle.producto_id)
                puntos_extra = (producto.puntos_extra) * detalle.cantidad
            except Producto.DoesNotExist:
                pass

            detalles.append({
                'nombre': detalle.nombre_producto,
                'cantidad': detalle.cantidad,
                'puntos_extra': puntos_extra,
            })
        pedidos_con_detalles.append({
            'pedido': pedido,
            'detalles': detalles,
        })

    return render(request, 'pedido/puntos_recompensas.html', {
        'perfil': perfil,
        'pedidos_con_detalles': pedidos_con_detalles,
    })




@csrf_exempt
def kiosko_pedido(request):
    productos = Producto.objects.filter(activo=True)
    sucursales = Sucursal.objects.all()
    mensaje = None
    VALOR_PUNTO = Decimal('0.50')

    if request.method == 'POST':
        sucursal_id = request.POST.get('sucursal')
        sucursal = Sucursal.objects.get(id=sucursal_id)
        carrito_json = request.POST.get('carrito_json')
        carrito = json.loads(carrito_json) if carrito_json else []
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        total = Decimal('0')
        for item in carrito:
            producto = Producto.objects.get(id=item['id'])
            cantidad = int(item['cantidad'])
            subtotal = producto.precio * cantidad
            total += subtotal

        if request.user.is_authenticated and hasattr(request.user, 'perfil'):
            perfil = request.user.perfil
            puntos_a_usar = int(request.POST.get('puntos_a_usar', 0))
            max_puntos = min(perfil.puntos, int(total // VALOR_PUNTO))
            puntos_a_usar = min(puntos_a_usar, max_puntos)
            total_final = total - (puntos_a_usar * VALOR_PUNTO)
            estado_pedido = 'pagado' if total_final == 0 else 'pendiente'
            pedido = Pedido.objects.create(
                usuario=request.user,
                sucursal=sucursal,
                estado=estado_pedido,
                total=total_final,
                puntos_usados=puntos_a_usar,
            )
            if puntos_a_usar > 0:
                perfil.puntos -= puntos_a_usar
                perfil.save()
        else:
          
            pedido = Pedido.objects.create(
                usuario=None,
                sucursal=sucursal,
                estado='pendiente',
                total=total,
                puntos_ganados=0,
                puntos_usados=0,
            )

        # Crea los detalles del pedido
        for item in carrito:
            producto = Producto.objects.get(id=item['id'])
            cantidad = int(item['cantidad'])
            subtotal = producto.precio * cantidad
            DetallePedido.objects.create(
                pedido=pedido,
                producto_id=producto.id,
                cantidad=cantidad,
                subtotal=subtotal,
            )

        PedidoPickup.objects.create(
            pedido=pedido,
            horario_recoleccion=timezone.now(),
            tipo_pago='kiosko',
        )

        if request.user.is_authenticated and hasattr(request.user, 'perfil') and pedido.total > 0:
            puntos_por_total = int(pedido.total // 30) * 5
            puntos_extra = sum([
                getattr(detalle.producto_id, 'puntos_extra', 0) * detalle.cantidad
                for detalle in pedido.detalles.all()
            ])
            total_puntos = puntos_por_total + puntos_extra
            perfil = request.user.perfil
            perfil.puntos += total_puntos
            perfil.save()
            pedido.puntos_ganados = total_puntos
            pedido.save()

        mensaje = f"¡Pedido realizado! Código: {pedido.codigo}"

        return render(request, 'pedido/kiosko_exito.html', {
            'pedido': pedido,
            'mensaje': mensaje,
            'nombre': nombre,
            'telefono': telefono,
        })

    return render(request, 'pedido/kiosko.html', {
        'productos': productos,
        'sucursales': sucursales,
        'categorias': Categoria.objects.filter(activo=True),  # Agregado para organizar productos
    })