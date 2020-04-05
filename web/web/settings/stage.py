from web.settings.base import *

assert SERVICE_ENVIRONMENT == 'stage', SERVICE_ENVIRONMENT

DEBUG = False

LOGGING.update({
    'disable_existing_loggers': False,
    'loggers': {
        'web': {
            'handlers': ['console'],
            'level': LOGGING_LEVEL,
        }
    }
})
