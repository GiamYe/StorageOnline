"""
Django settings for ypan project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!69+r^dxp9&#eo70c=^p3138ib-tkdv&u2#nyi37=3^vey8rz4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'disk',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ypan.urls'

WSGI_APPLICATION = 'ypan.wsgi.application'

API_URL = 'http://127.0.0.1:5000'

LOGIN_URL = '/signin/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yunpan',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST':'127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/web/'
MEDIA_URL = os.path.join(BASE_DIR,'file/')
MEDIA_ROOT = os.path.join(BASE_DIR, STATIC_URL.replace("/", ""))

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'web/views'),
    os.path.join(BASE_DIR, 'web/views/layout'),
)

STATICFILES_DIRS = (
    MEDIA_ROOT,
)
