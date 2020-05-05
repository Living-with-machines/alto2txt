"""
Logging utilities.
"""

import logging


def configure_logging(log_file):
    """
    Configure console and file logging.

    :param log_file: log file
    :type log_file: str 
    """
    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(process)d:%(levelname)s:%(message)s",
        style="%")
    logging.basicConfig(level=logging.INFO,
                        formatter=formatter)
    file_logger = logging.FileHandler(log_file)
    file_logger.setLevel(logging.INFO)
    file_logger.setFormatter(formatter)
    logging.getLogger().addHandler(file_logger)
