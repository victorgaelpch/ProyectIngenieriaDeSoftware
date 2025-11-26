# menu/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Producto, Categoria, Subcategoria, AtributoSubcategoria
from .forms import ProductoForm
from django.core.files.storage import default_storage
from django.conf import settings
import uuid
import os

def es_gerente(user):
    return user.is_authenticated and user.groups.filter(name='Gerente').exists()

def lista_productos(request):
    categoria_id = request.GET.get('categoria')
    subcategoria_id = request.GET.get('subcategoria')
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.filter(activo=True)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if subcategoria_id:
        productos = productos.filter(subcategoria_id=subcategoria_id)

    es_gerente_flag = request.user.is_authenticated and request.user.groups.filter(
        name='Gerente').exists()

    # Resolver atributos legibles e inyectarlos en cada producto
    productos_con_atributos = []
    for p in productos:
        atributos_legibles = []
        if p.atributos:
            for key, value in p.atributos.items():
                try:
                    atributo = AtributoSubcategoria.objects.get(id=key)
                    atributos_legibles.append({
                        'nombre': atributo.nombre,
                        'valor': value
                    })
                except AtributoSubcategoria.DoesNotExist:
                    atributos_legibles.append({
                        'nombre': key,
                        'valor': value
                    })
        productos_con_atributos.append({
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'precio': p.precio,
           
            'imagen': p.imagen if p.imagen else None,
      
            'stock': p.stock,
            'activo': p.activo,
            'atributos_legibles': atributos_legibles,
        })

    context = {
        'productos': productos_con_atributos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
        'subcategoria_seleccionada': subcategoria_id,
        'es_gerente': es_gerente_flag,
    }

    return render(request, 'menu/lista_productos.html', context)


@user_passes_test(es_gerente)
def agregar_producto(request):
    es_gerente_flag = es_gerente(request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES) # Asegúrate de incluir request.FILES
        print("Datos del formulario POST:", request.POST)
        print("Archivos del formulario FILES:", request.FILES)
        if form.is_valid():
            # --- MANEJO DE IMAGEN ---
            print("Formulario válido. Procesando imagen...")
            imagen_guardada_path = None # Inicializar variable
            imagen_file = getattr(form, 'cleaned_imagen_file', None) # Obtener el archivo subido

            if imagen_file:
                # Generar un nombre único para evitar conflictos
                nombre_original = imagen_file.name
                print("Nombre original de la imagen subida:", nombre_original)
                nombre_base, extension = os.path.splitext(nombre_original)
                nombre_unico = f"{uuid.uuid4()}{extension}"
                # Definir la ruta donde se guardará (dentro de MEDIA_ROOT)
                ruta_relativa_destino = os.path.join('imgProductos', nombre_unico) # Carpeta 'productos' dentro de 'media'
                ruta_absoluta_destino = os.path.join(settings.MEDIA_ROOT, ruta_relativa_destino)
                print("Rutare relativa destino:", ruta_relativa_destino)
                # Crear directorios si no existen
                os.makedirs(os.path.dirname(ruta_absoluta_destino), exist_ok=True)

                # Guardar el archivo físicamente
                try:
                    with open(ruta_absoluta_destino, 'wb+') as destination:
                        for chunk in imagen_file.chunks():
                            destination.write(chunk)
                    # Guardamos la ruta RELATIVA para almacenarla en Cassandra como string
                    imagen_guardada_path = ruta_relativa_destino
                except Exception as e:
                    messages.error(request, f'Error al guardar la imagen localmente: {e}')
                    # Retorna el formulario con errores o maneja como prefieras
                    return render(request, 'menu/agregar_producto.html', {'form': form, 'es_gerente': es_gerente_flag})
            # --- FIN MANEJO DE IMAGEN ---

            # Crear instancia del modelo desde el form, pero no guardar aún
            producto = form.save(commit=False) # commit=False evita que se guarde inmediatamente
            # Asignar la ruta relativa de la imagen guardada (o None si no se subió)
            # Este es el paso CRUCIAL: asignas una STRING a imagen
            print("Imagen guardada en ruta:", imagen_guardada_path)
            producto.imagen = imagen_guardada_path
            # Ahora sí, guardar en Cassandra
            try:
                producto.save()
                messages.success(request, 'Producto agregado exitosamente.')

                # Manejar atributos dinámicos después de guardar el producto
                if producto.subcategoria_id:
                    atributos_actualizados = {}
                    for key, value in request.POST.items():
                        if key.startswith('atributo_') and value.strip():
                            atributo_id = key.replace('atributo_', '')
                            # Guardar en el campo atributos del producto
                            atributos_actualizados[atributo_id] = value.strip()
                    if atributos_actualizados:
                        producto.atributos = atributos_actualizados
                        producto.save() # Guardar de nuevo con los atributos

                # Redirigir según acción
                if 'action' in request.POST and request.POST['action'] == 'save_and_add':
                    return redirect('menu:agregar_producto') # Volver al formulario vacío
                else:
                    return redirect('menu:producto_list') # Ir a la lista
            except Exception as e:
                # Si la imagen se guardó pero falla el modelo, borrar la imagen
                if imagen_guardada_path and os.path.exists(os.path.join(settings.MEDIA_ROOT, imagen_guardada_path)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, imagen_guardada_path))
                messages.error(request, f'Error al guardar el producto en la base de datos: {e}')
                # Retorna el formulario con errores o maneja como prefieras
                return render(request, 'menu/agregar_producto.html', {'form': form, 'es_gerente': es_gerente_flag})
        else:
            print("Formulario inválido. Errores:", form.errors)
    else: # Método GET
        
        form = ProductoForm()
    return render(request, 'menu/agregar_producto.html', {'form': form, 'es_gerente': es_gerente_flag})


@user_passes_test(es_gerente)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    es_gerente_flag = es_gerente(request.user)

    # Guardar la ruta de la imagen anterior
    imagen_anterior_path = producto.imagen

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto) # Asegúrate de incluir request.FILES
        if form.is_valid():
            # --- MANEJO DE IMAGEN (similar al agregar, pero considerando la imagen anterior) ---
            imagen_anterior_path_para_borrar = imagen_anterior_path # Copia para posible borrado
            imagen_guardada_path = imagen_anterior_path # Por defecto, mantener la anterior
            imagen_file = request.FILES.get('imagen')

            if imagen_file: # Si se subió una nueva imagen
                # Borrar la imagen anterior si existía
                if imagen_anterior_path_para_borrar and os.path.exists(os.path.join(settings.MEDIA_ROOT, imagen_anterior_path_para_borrar)):
                    try:
                        os.remove(os.path.join(settings.MEDIA_ROOT, imagen_anterior_path_para_borrar))
                    except OSError as e:
                        # Opcional: Loggear el error o mostrar un mensaje
                        print(f"Error al borrar imagen anterior {imagen_anterior_path_para_borrar}: {e}")

                # Generar nuevo nombre y guardar (igual que en agregar)
                nombre_original = imagen_file.name
                nombre_base, extension = os.path.splitext(nombre_original)
                nombre_unico = f"{uuid.uuid4()}{extension}"
                ruta_relativa_destino = os.path.join('productos', nombre_unico)
                ruta_absoluta_destino = os.path.join(settings.MEDIA_ROOT, ruta_relativa_destino)

                os.makedirs(os.path.dirname(ruta_absoluta_destino), exist_ok=True)

                try:
                    with open(ruta_absoluta_destino, 'wb+') as destination:
                        for chunk in imagen_file.chunks():
                            destination.write(chunk)
                    imagen_guardada_path = ruta_relativa_destino # Ruta nueva
                except Exception as e:
                    messages.error(request, f'Error al guardar la nueva imagen: {e}')
                    return render(request, 'menu/editar_producto.html', {'form': form, 'producto': producto, 'es_gerente': es_gerente_flag})

            # --- FIN MANEJO DE IMAGEN ---

            producto = form.save(commit=False) # No guardar aún
            producto.imagen = imagen_guardada_path # Asignar la nueva ruta o la anterior como STRING
            producto.save() # Ahora sí guardar

            # Manejar atributos dinámicos
            atributos_actualizados = {}
            if producto.subcategoria_id:
                for key, value in request.POST.items():
                    if key.startswith('atributo_') and value.strip():
                        atributo_id = key.replace('atributo_', '')
                        atributos_actualizados[atributo_id] = value.strip()

            producto.atributos = atributos_actualizados
            producto.save()

            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('menu:producto_list')
    else: # Método GET
        form = ProductoForm(instance=producto)

    return render(request, 'menu/editar_producto.html', {'form': form, 'producto': producto, 'es_gerente': es_gerente_flag})

@user_passes_test(es_gerente)
def eliminar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        # Borrar la imagen asociada si existe
        if producto.imagen and os.path.exists(os.path.join(settings.MEDIA_ROOT, producto.imagen)):
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, producto.imagen))
            except OSError as e:
               
                print(f"Error al borrar imagen del producto eliminado {producto.imagen}: {e}")
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe.')
    return redirect('menu:producto_list')
