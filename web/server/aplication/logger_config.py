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
            'filename': 'log',
            'maxBytes': 1000000,
            'backupCount': 3,
        },
    },
    'loggers': {
        'RequestLogger': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
}