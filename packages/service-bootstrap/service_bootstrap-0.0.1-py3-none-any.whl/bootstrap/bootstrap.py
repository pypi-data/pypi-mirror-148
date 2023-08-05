import logging
import os
from logging import config as logging_config

import tzlocal
import yaml


def start_service():
    with open("logging.yaml", 'r') as f:
        config = yaml.full_load(f)
    logging_config.dictConfig(config)

    logger = logging.getLogger("main")
    logger.info("Starting application!")

    config_file = os.getenv('CONFIG', 'config/config.yaml')

    with open(config_file, 'r') as f:
        config = yaml.full_load(f)

    timezone = os.getenv('TIMEZONE', str(tzlocal.get_localzone()))

    return config, logger, timezone
