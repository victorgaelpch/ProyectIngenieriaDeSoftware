"""
URL configuration for miLogin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('miInicio.urls')),
    path('', include('perfil.urls'), name='perfil'),
    path('', include('pedido.urls'), name='pedido'),
    path('', include('menu.urls'), name='menu'),
    path('', include('gestion.urls'), name='gestion'),
    path('', include('administracion.urls'), name='administracion'),
    path('', include('caja.urls'), name='caja'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('administracion.urls'), name='administracion'),
    # Cambio de contraseña
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='passwordReset/password_change.html',
        success_url='/perfil/'
    ), name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='passwordReset/password_change_done.html'
    ), name='password_change_done'),

    # Reset / recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='passwordReset/password_reset.html',
        email_template_name='passwordReset/password_reset_email.html',
        success_url='/password_reset/done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='passwordReset/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='passwordReset/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='passwordReset/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('', include('django_prometheus.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)