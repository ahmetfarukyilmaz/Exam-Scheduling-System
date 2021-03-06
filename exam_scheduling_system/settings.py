"""
Django settings for exam_scheduling_system project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%+l)els(1@^#8+6o@62z2&*mgqyvo45)yb-_)get^_w5x4jyc*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'exam',
    'phonenumber_field',
    'tempus_dominus',
    'datetimewidget',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'exam_scheduling_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'exam_scheduling_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'exam_scheduling_system',
        'USER':'examsystem',
        'PASSWORD':'examsystem123',
        'HOST':'examschedulingsystem.ctphni9y5upc.us-east-2.rds.amazonaws.com',
        'PORT':'5432'
    }
} """

#LOCAL DATABASE
DATABASES = {
    'default':{
       'ENGINE':'django.db.backends.postgresql_psycopg2',
       'NAME':'postgres',
       'USER':'postgres',
       'PASSWORD':'123',
       'HOST':'localhost',
       'POST':'5432',
        'ATOMATIC_REQUESTS':True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators


#PASSWORD VALIDATION DISABLED ONLY FOR DEVELOPMENT
AUTH_PASSWORD_VALIDATORS = [
    
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'static')
       ]
else:
        STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_URL='/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#Email Settings
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER= 'exam.scheduling.system@gmail.com'
EMAIL_HOST_PASSWORD='exam_scheduling_system'
EMAIL_USE_TLS=True
EMAIL_USE_SSL = False

