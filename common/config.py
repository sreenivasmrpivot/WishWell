# config.py

import logging
import configparser

def setup_logging_from_file(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    log_level = config['LOGGING']['Level']
    logging.basicConfig(level=getattr(logging, log_level, 'INFO'))

def setup_logging_from_args(log_level):
    logging.basicConfig(level=getattr(logging, log_level, 'INFO'))
