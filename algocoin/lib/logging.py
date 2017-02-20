import os
import os.path
import logging.config

if not os.path.isdir('./logs'):
    os.mkdir('./logs')

LOGGING_CONFIG = {
    'version': 1,  # required
    'disable_existing_loggers': True,  # this config overrides all other loggers
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s -- %(message)s'
        },
        'whenAndWhere': {
            'format': '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'whenAndWhere'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/out.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_strat': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/strat.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_errors': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/errors.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_data': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/data.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_transaction': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/txns.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_manual': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/manual.log',
            'mode': 'w',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {  # 'root' logger
            'level': 'CRITICAL',
            'handlers': ['console', 'file']
        },
        'other': {
            'level': 'CRITICAL',
            'handlers': ['file']
        },
        'strat': {
            'level': 'CRITICAL',
            'handlers': ['file_strat']
        },
        'errors': {
            'level': 'CRITICAL',
            'handlers': ['file_errors']
        },
        'data': {
            'level': 'CRITICAL',
            'handlers': ['file_data']
        },
        'transaction': {
            'level': 'CRITICAL',
            'handlers': ['file_transaction']
        },
        'manual': {
            'level': 'CRITICAL',
            'handlers': ['file_manual']
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
LOG = logging.getLogger('')  # factory method
OTHER = logging.getLogger('other')
STRAT = logging.getLogger('strat')
WARN = logging.getLogger('errors')
ERROR = logging.getLogger('errors')
DATA = logging.getLogger('data')
TXN = logging.getLogger('transaction')
MANUAL = logging.getLogger('manual')

OTHER.propagate = False
STRAT.propagate = False
WARN.propagate = False
ERROR.propagate = False
DATA.propagate = False
TXN.propagate = False
MANUAL.propagate = False

OTHER.setLevel(logging.CRITICAL)
STRAT.setLevel(logging.CRITICAL)
WARN.setLevel(logging.CRITICAL)
ERROR.setLevel(logging.CRITICAL)
DATA.setLevel(logging.CRITICAL)
TXN.setLevel(logging.CRITICAL)
MANUAL.setLevel(logging.CRITICAL)
