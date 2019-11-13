import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'botlog',
            'maxBytes': 100000,
            'backupCount': 3,
        },
    },
    'loggers': {
        'BotLogger': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

logger = logging.getLogger('BotLogger')
logging.config.dictConfig(LOGGING_CONFIG)
