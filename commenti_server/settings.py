from pathlib import Path
import os
from datetime import timedelta

SECRET_KEY = os.environ.get('COMMENTI_SECRET_KEY', 'my-secure-secret-key')
DEBUG = os.environ.get('COMMENTI_DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS = [os.environ.get('COMMENTI_ALLOWED_HOST', '*')]


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.environ.get('COMMENTI_STATIC_ROOT', BASE_DIR.parent / 'static')

STATIC_URL = '/static/'


CORS_ALLOWED_ORIGIN_REGEXES = [
    os.environ.get('COMMENTI_CORS_ALLOWED_ORIGIN_REGEX', '^.*$')
]
CORS_URLS_REGEX = r'^/graphql/?$'

# SQLite isn't recommended, this option is for CI/CD
DATABASE = os.environ.get('COMMENTI_DATABASE', 'sqlite3')

# Application definition

INSTALLED_APPS = [
    'comments.apps.CommentsConfig',
    'commenti_server.apps.CommentiAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'corsheaders',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
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
            'NAME':     os.environ['COMMENTI_DATABASE_NAME'],
            'USER':     os.environ['COMMENTI_DATABASE_USER'],
            'PASSWORD': os.environ['COMMENTI_DATABASE_PASSWORD'],
            'HOST':     os.environ['COMMENTI_DATABASE_HOST'],
            'PORT': int(os.environ['COMMENTI_DATABASE_PORT']),
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

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
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
    "SCHEMA": "commenti_server.schema.schema",
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

GRAPHQL_JWT = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(minutes=int(os.environ.get('COMMENTI_ACCESS_TOKEN_EXPIRATION_MINUTES', 5))),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=int(os.environ.get('COMMENTI_REFRESH_TOKEN_EXPIRATION_DAYS', 90))),
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
}
