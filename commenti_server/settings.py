from pathlib import Path
import os
from django.db import models

SECRET_KEY = os.environ.get('SECRET_KEY', 'my-secure-secret-key')
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', '*')]


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.environ.get('STATIC_ROOT', BASE_DIR.parent / 'static')

STATIC_URL = '/static/'


CORS_ALLOWED_ORIGIN_REGEXES = [
    os.environ.get('CORS_ALLOWED_ORIGIN_REGEX', '^.*$')
]
CORS_URLS_REGEX = r'^/graphql/?$'

# SQLite isn't recommended, this option is for CI/CD
DATABASE = os.environ.get('DATABASE', 'sqlite3')

# Application definition

INSTALLED_APPS = [
    'comments.apps.CommentsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'commenti_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'commenti_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if DATABASE == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'database',
        }
    }
elif DATABASE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     os.environ['DATABASE_NAME'],
            'USER':     os.environ['DATABASE_USER'],
            'PASSWORD': os.environ['DATABASE_PASSWORD'],
            'HOST':     os.environ['DATABASE_HOST'],
            'PORT': int(os.environ['DATABASE_PORT']),
        }
    }
else:
    raise RuntimeError('Invalid Django database configuration')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# GraphQL
GRAPHENE = {
    "SCHEMA": "commenti_server.schema.schema"
}
