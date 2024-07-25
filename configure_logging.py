import logging


def configure_logging_with_file(log_file: str, level: str = "DEBUG") -> logging.Logger:
    """
    Configure logging.
    :param log_file: Log file name.
    :param level: Set log level.
    :return: None.
    """
    # Remove any existing basicConfig handlers
    logging.getLogger().handlers.clear()

    # Get the root logger
    logger = logging.getLogger()

    # Set the logging level
    if level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif level == "INFO":
        logger.setLevel(logging.INFO)
    elif level == "WARNING":
        logger.setLevel(logging.WARNING)
    elif level == "ERROR":
        logger.setLevel(logging.ERROR)
    elif level == "CRITICAL":
        logger.setLevel(logging.CRITICAL)

    # Define a custom log format
    log_format = '%(asctime)s | %(filename)s | line:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s'

    # Create a FileHandler to write logs to the specified file in overwrite mode
    file_handler = logging.FileHandler(log_file, mode='w')  # 'w' for write mode (overwrite)

    # Create a StreamHandler to output logs to the terminal
    stream_handler = logging.StreamHandler()

    # Create a Formatter with the custom log format
    formatter = logging.Formatter(log_format)

    # Set the Formatter for both the FileHandler and StreamHandler
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add both the FileHandler and StreamHandler to the root logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger