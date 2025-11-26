"""vistas de miInicio"""
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def es_gerente(user):
    return user.is_authenticated and user.groups.filter(name='Gerente').exists()


def home(request):
    """funcion de inicio"""
    return render(request, 'Principal/home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'Principal/signup.html', {
            'form': CustomUserCreationForm()
        })
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ver_perfil')
        else:
            return render(request, 'Principal/signup.html', {
                'form': form
            })


@login_required
def cerrar_sesion(request):
    """funcion de cerrar sesion"""
    logout(request)
    return redirect('home')


def inicio_sesion(request):
    """funcion de inicio de sesion"""
    if request.method == 'GET':
        return render(request, 'Principal/signin.html', {
            'form': AuthenticationForm()
        })
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if user.is_authenticated:
                if user.is_staff:
                    return redirect('caja:caja_buscar_pedido')
                else:
                    return redirect('ver_perfil')
        return render(request, 'Principal/signin.html', {
            'form': form,
            'error': 'Usuario o contraseña incorrecto'
        })
