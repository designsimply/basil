""" Settings module, uses a different paradigm from django

config based on yaml with ability to overwrite in environment


CONFIG_PATH = ./config/

CONFIG_FILES = 'base.yaml'

Then it loads ./config/base.yaml

Which is a nested dictionary. Then it loads from the environment based on
nested keys.

DJANGO__level1_key__level2_key: value


"""

import os

# ############################################################################ #
#
# Relative paths
#
# ############################################################################ #


# /opt/app/
BASE_DIR = os.path.dirname(
    os.path.dirname(
        __file__
    )
)

# /opt/app
APP_DIR = os.path.join(BASE_DIR, 'app')


# ############################################################################ #
#
# Base settings
#
# ############################################################################ #


# OVERWRITE SETTINGS USING
#
# ENV DJANGO__<name>_
#

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*)s9o+=wjhxn1*1+_ssymqh@rrp#ylko6=9&en*5_enblgy)g5'

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
    'helloworld',
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

ROOT_URLCONF = 'config.urls'


TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            TEMPLATE_DIR
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


WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
  'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stuffdb',
        'USER': 'basil',
        'PASSWORD': 'DJANGO__DATABASES__default__PASSWORD',
        'HOST': 'postgres',
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

STATIC_URL = '/static/'


# ############################################################################ #
#
# Load environment variables
#
# ############################################################################ #


def _get_env(setting):
    """ Read an environment file and load.

    """
    value = os.environ[setting]

    # Boolean values
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False

    # floats
    if '.' in value:
        try:
            return float(value)
        except ValueError:
            pass

    # integers
    try:
        return int(value)
    except ValueError:
        pass

    # list
    if ':' in value:
        return value.split(':')

    # string
    return value


def _recursive_load_from_env(config, key_list=None):
    """ Load from the environment

    ENV DJANGO__key1___0___key2: True

    This will update config['key1'][0]['key2'] = True

    Parameters
        config (dict): nested dict of variables
        key_list (list): recursive keys

    """
    if key_list is None:
        key_list = []
        value = config
    else:
        key = key_list[-1]

        env_name = '__'.join(['DJANGO'] + [str(k) for k in key_list])
        if env_name in os.environ:
            print(f'found env key {env_name}')
            config[key] = _get_env(env_name)
            return config

        value = config[key]

    if isinstance(value, dict):
        for nested_key in value:
            if isinstance(nested_key, str) and nested_key.startswith('_'):
                continue
            _recursive_load_from_env(value, key_list + [nested_key])
        return value
    elif isinstance(value, list):
        for i in range(len(value)):
            _recursive_load_from_env(value, key_list + [i])
        return value

    else:
        # t = type(value)
        # raise TypeError(f'Invalid type {t} with {value}')
        return config


# add all _config to the globals of this module
globals().update(_recursive_load_from_env(globals()))
