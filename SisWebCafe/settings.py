from pathlib import Path
from decouple import config, Csv
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = ['*']

SITE_ID = 1


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_cassandra_engine',
    'crispy_forms',
    'crispy_bootstrap4',
    'widget_tweaks',
    # monitoring
    "django_prometheus",
    # local apps
    'miInicio',
    'pedido',
    'perfil',
    'menu',
    'administracion',
    'gestion',
    'caja',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'SisWebCafe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'SisWebCafe.context_processors.es_gerente',
                'administracion.context_processors.theme_context',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'SisWebCafe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""

DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DBP_NAME'),
        'USER': config('DBP_USER'),
        'PASSWORD': config('DBP_PASSWORD'),
        'HOST': config('DBP_HOST'),  
        'PORT': config('DBP_PORT'),  
    },
    'cassandra': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': config('DBC_NAME'),
        'TEST_NAME': config('DBC_TEST_NAME'),
        'HOST': config('DBC_HOST',cast=str),
        'PORT': 9042,
        'OPTIONS': {
            'replication': {'strategy_class': 'SimpleStrategy','replication_factor': 3,},
            
       
        }
    }


    
}
# Router para manejar lecturas/escrituras
DATABASE_ROUTERS = ['SisWebCafe.routers.CassandraRouter']
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = 'home'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
