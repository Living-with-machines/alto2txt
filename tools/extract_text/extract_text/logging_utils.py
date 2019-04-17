"""
Logging utilities.
"""

import logging


def configure_logging(log_file):
    """
    Configure logging.

    :param log_file: log file
    :type log_file: str or unicode
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_logger)
    file_logger = logging.FileHandler(log_file)
    file_logger.setLevel(logging.INFO)
    logging.getLogger().addHandler(file_logger)
