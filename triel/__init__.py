import logging.config

from triel.resources import resource_path


def configure_log():
    logging.config.fileConfig(resource_path("log_config.ini"))


configure_log()
