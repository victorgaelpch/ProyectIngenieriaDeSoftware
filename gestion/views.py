from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from pedido.models import Sucursal
from .forms import SucursalForm


def es_gerente(user):
    return user.is_authenticated and user.groups.filter(name='Gerente').exists()


@user_passes_test(es_gerente)
def lista_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'gestion/lista_sucursales.html', {'sucursales': sucursales})


@user_passes_test(es_gerente)
def agregar_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_sucursales')
    else:
        form = SucursalForm()
    return render(request, 'gestion/agregar_sucursal.html', {'form': form})


@user_passes_test(es_gerente)
def editar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('lista_sucursales')
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'gestion/editar_sucursal.html', {'form': form, 'sucursal': sucursal})


@user_passes_test(es_gerente)
def eliminar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('lista_sucursales')
    return render(request, 'gestion/eliminar_sucursal.html', {'sucursal': sucursal})
