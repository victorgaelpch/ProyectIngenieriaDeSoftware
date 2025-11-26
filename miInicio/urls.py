from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('signin/', views.inicio_sesion, name="signin"),
    # otras rutas que tengas en miInicio
]
