"""Logging configuration for ProtecView application"""

import logging
import logging.config
import logging.handlers
import os

def _get_log_path():
    """Get log file path from env or default to logs/ directory"""
    log_dir = os.environ.get('PROTECVIEW_LOG_DIR', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, 'protecview.log')

_LOG_PATH = _get_log_path()
_LOG_LEVEL = os.environ.get('PROTECVIEW_LOG_LEVEL', 'INFO').upper()

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': _LOG_LEVEL,
            'formatter': 'detailed',
            'filename': _LOG_PATH,
            'maxBytes': 10485760,
            'backupCount': 5,
            'encoding': 'utf-8'
        },
    },
    'root': {
        'level': _LOG_LEVEL,
        'handlers': ['console', 'file']
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'callbacks': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'utils': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    }
}


def setup_logging():
    """Configure logging for the application"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("ProtecView logging initialized")
    return logger
