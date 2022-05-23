'''
Django settings for server project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
'''

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+wje&f9i^p8e#223@b#)3a2ersul)5vl8dbtdq1p0e7m61+28a'

DEBUG = True
ALLOWED_HOSTS = ['*']

# The “sites” framework
# https://docs.djangoproject.com/en/4.0/ref/contrib/sites/

SITE_ID = 1

# Application definition
SHARED_APPS = (
    # Django Apps
    'django_tenants',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Multi Tenancy Apps
    'tenant_users.permissions',
    'tenant_users.tenants',
    'django_extensions',
    'crispy_forms',
    # Project Apps
    'account',
    'membership',
)

TENANT_APPS = (
    # Django Apps
    'django.contrib.auth',  # Defined in both shared apps and tenant apps
    'django.contrib.contenttypes',  # Defined in both shared apps and tenant apps
    # Multi Tenancy Apps
    'tenant_users.permissions',  # Defined in both shared apps and tenant apps
    # Project Apps
    'blog',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = 'membership.Client'
TENANT_DOMAIN_MODEL = 'membership.Domain'
TENANT_USERS_DOMAIN = 'example.com'
TENANT_SUBFOLDER_PREFIX = 'r'
# SESSION_COOKIE_DOMAIN = '.localhost'

ROOT_URLCONF = 'server.urls_tenants'
PUBLIC_SCHEMA_URLCONF = 'server.urls_public'

MIDDLEWARE = [
    # 'django_tenants.middleware.main.TenantMainMiddleware',
    # 'django_tenants.middleware.TenantSubfolderMiddleware',
    'server.middleware.TenantSubfolderMiddleware',
    # 'server.middleware.TenantInactiveMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ROOT_URLCONF = 'server.urls'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'tenant_user',
        'USER': 'c0d3',
        'PASSWORD': 'Anon@ha4er',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Auth
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/

AUTH_USER_MODEL = 'account.User'
PASSWORD_RESET_TIMEOUT = 86400

AUTHENTICATION_BACKENDS = (
    'tenant_users.permissions.backend.UserBackend',
)

# Login function

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# django-tenants & django-tenant-users
# https://github.com/django-tenants/django-tenants
# https://github.com/Corvia/django-tenant-users


# django_extensions settings
# https://github.com/django-extensions/django-extensions/blob/main/docs/shell_plus.rst#additional-imports

SHELL_PLUS_IMPORTS = [
    # 'from tenant_users.tenants.utils import create_public_tenant',
    'from tenant_users.tenants.tasks import provision_tenant',
    'from server.init_tenant import create_public_tenant',
    'from account.models import User, Client, Domain',
]


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = (
    BASE_DIR / 'assets',
)

# Media Files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
