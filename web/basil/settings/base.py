""" Settings module, uses a different paradigm from django
"""

import os

# ############################################################################ #
#
# Relative paths
#
# ############################################################################ #


# /code/
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            __file__
        )
    )
)

# /code/apps
APPS_DIR = os.path.join(BASE_DIR, 'apps')


# ############################################################################ #
#
# Base settings
#
# ############################################################################ #

SERVICE_ENVIRONMENT = os.environ['SERVICE_ENVIRONMENT']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'links',
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

ROOT_URLCONF = 'basil.urls'

_TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            _TEMPLATES_DIR,
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    }
]


WSGI_APPLICATION = 'basil.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['POSTGRES_HOST'],
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'  # noqa
    }
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static Content
# https://docs.djangoproject.com/en/3.0/ref/settings/#static-files

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'untracked_static')
STATICFILES_DIRS = [
    os.path.join(_TEMPLATES_DIR, 'static'),
]

# API

MAX_PER_PAGE = 50


# Logging

LOGGING_LEVEL = os.environ.get('DJANGO_LOGGING_LEVEL', 'DEBUG')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '{asctime} {process} {module:10}:L{lineno} '
                '{levelname:8} \n {message}'
            ),
            'style': '{'
        },
        'default': {
            'format': '{levelname} | {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'root': {
        'level': LOGGING_LEVEL,
        'handlers': ['console']
    },
    'loggers': {
        'webserver': {
            'handlers': ['console'],
            'level': LOGGING_LEVEL,
        }
    }
}
