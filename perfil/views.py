from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pedido.models import PerfilUsuario
from perfil.models import DireccionFacturacion
from .forms import PerfilUsuarioForm, DireccionFacturacionForm, UserForm


@login_required
def ver_perfil(request):
    direcciones = request.user.direcciones_facturacion.all()
    perfil = request.user.perfil
    return render(request, 'perfil/perfil.html', {
        'perfil': perfil,
        'direcciones': direcciones
    })


@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    direcciones = request.user.direcciones_facturacion.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, instance=perfil)
        direccion_form = DireccionFacturacionForm(request.POST)

        if 'guardar_perfil' in request.POST:
            if user_form.is_valid() and perfil_form.is_valid():
                user_form.save()
                perfil_form.save()
                return redirect('ver_perfil')

        elif 'agregar_direccion' in request.POST:
            if direccion_form.is_valid():
                nueva_direccion = direccion_form.save(commit=False)
                nueva_direccion.usuario = request.user
                nueva_direccion.save()
                return redirect('editar_perfil')
    else:
        user_form = UserForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfil)
        direccion_form = DireccionFacturacionForm()

    return render(request, 'perfil/editarPerfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'direccion_form': direccion_form,
        'direcciones': direcciones,
    })


@login_required
def editar_direccion(request, direccion_id):
    try:
        direccion = DireccionFacturacion.objects.get(
            id=direccion_id, usuario=request.user)
    except DireccionFacturacion.DoesNotExist:
        return redirect('editar_perfil')

    if request.method == 'POST':
        form = DireccionFacturacionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            return redirect('editar_perfil')
    else:
        form = DireccionFacturacionForm(instance=direccion)

    return render(request, 'perfil/editarDireccion.html', {
        'form': form,
        'direccion': direccion,
    })


@login_required
def eliminar_direccion(request, direccion_id):
    try:
        direccion = DireccionFacturacion.objects.get(
            id=direccion_id, usuario=request.user)
        direccion.delete()
    except DireccionFacturacion.DoesNotExist:
        pass 

    return redirect('editar_perfil')
