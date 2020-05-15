"""
Logging utilities.
"""

import logging


def configure_logging(log_file):
    """
    Configure console and file logging.

    :param log_file: log file
    :type log_file: str or unicode
    """

    #format = "%(asctime)s:%(name)s:%(process)d:%(levelname)s:%(message)s"
 
    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(process)d:%(levelname)s:%(message)s",
        style="%")
  
    logging.basicConfig(level=logging.INFO,
                        format=format)
    file_logger = logging.FileHandler(log_file)
    file_logger.setLevel(logging.INFO)
    file_logger.setFormatter(format)
    logging.getLogger().addHandler(file_logger)
