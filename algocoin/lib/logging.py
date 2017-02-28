import os
import os.path
import logging.config

if not os.path.isdir('./logs'):
    os.mkdir('./logs')

LOGGING_CONFIG = {
    'version': 1,  # required
    'disable_existing_loggers': False,
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

        'file_data': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/data.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_risk': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/risk.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_execution': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/exec.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_slippage': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/slip.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'file_transaction_costs': {
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
        },
        'file_errors': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'whenAndWhere',
            'filename': 'logs/errors.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        '': {  # 'root' logger
            'level': 'CRITICAL',
            'handlers': ['console', 'file']
        },
        'strat': {
            'level': 'CRITICAL',
            'handlers': ['file_strat']
        },
        'data': {
            'level': 'CRITICAL',
            'handlers': ['file_data']
        },
        'risk': {
            'level': 'CRITICAL',
            'handlers': ['file_risk']
        },
        'execution': {
            'level': 'CRITICAL',
            'handlers': ['file_execution']
        },
        'slippage': {
            'level': 'CRITICAL',
            'handlers': ['file_slippage']
        },
        'transactionCost': {
            'level': 'CRITICAL',
            'handlers': ['file_transaction_costs']
        },
        'manual': {
            'level': 'CRITICAL',
            'handlers': ['file_manual']
        },
        'errors': {
            'level': 'CRITICAL',
            'handlers': ['file_errors']
        },

    }
}

logging.config.dictConfig(LOGGING_CONFIG)
LOG = logging.getLogger('')  # factory method
STRAT = logging.getLogger('strat')
DATA = logging.getLogger('data')
RISK = logging.getLogger('risk')
EXEC = logging.getLogger('execution')
SLIP = logging.getLogger('slippage')
TXNS = logging.getLogger('transactionCost')
MANUAL = logging.getLogger('manual')
ERROR = logging.getLogger('errors')

STRAT.propagate = False
DATA.propagate = False
RISK.propagate = False
EXEC.propagate = False
SLIP.propagate = False
TXNS.propagate = False
MANUAL.propagate = False
ERROR.propagate = False

STRAT.setLevel(logging.CRITICAL)
DATA.setLevel(logging.CRITICAL)
RISK.setLevel(logging.CRITICAL)
EXEC.setLevel(logging.CRITICAL)
SLIP.setLevel(logging.CRITICAL)
TXNS.setLevel(logging.CRITICAL)
MANUAL.setLevel(logging.CRITICAL)
ERROR.setLevel(logging.CRITICAL)
