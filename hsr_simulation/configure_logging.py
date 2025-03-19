import logging
import os


def configure_logging_with_file(
    log_dir: str, log_file: str, logger_name: str, level: str = "DEBUG"
) -> logging.Logger:
    """
    Configure logging.
    :param log_dir: Directory for log file.
    :param log_file: Log file name.
    :param logger_name: Name of the logger.
    :param level: Set log level.
    :return: Logger object.
    """
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Full path to the log file
    log_file_path = os.path.join(log_dir, log_file)

    # Get the specified logger
    logger = logging.getLogger(logger_name)

    # Remove any existing handlers
    logger.handlers.clear()

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
    log_format = "%(asctime)s | %(filename)s | line:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s"

    # Create a FileHandler to write logs to the specified file in overwrite mode
    file_handler = logging.FileHandler(
        log_file_path, mode="w"
    )  # 'w' for write mode (overwrite)

    # Create a StreamHandler to output logs to the terminal
    stream_handler = logging.StreamHandler()

    # Create a Formatter with the custom log format
    formatter = logging.Formatter(log_format)

    # Set the Formatter for both the FileHandler and StreamHandler
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add both the FileHandler and StreamHandler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


main_logger = configure_logging_with_file(
    log_dir="logs", log_file="main.log", logger_name="main", level="WARNING"
)
