import logging
global logger


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    green = "\x1b[0;32m"
    green_intense = "\x1b[0;92m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[0;94m"
    reset = "\x1b[0m"
    log_text_format: str = "%(asctime)s - %(name)s - %(levelname)s - [%(className)s] - %(message)s"  # type: ignore

    FORMATS = {
        logging.DEBUG: grey + log_text_format + reset,
        logging.INFO: green_intense + log_text_format + reset,
        logging.WARNING: yellow + log_text_format + reset,
        logging.ERROR: red + log_text_format + reset,
        logging.CRITICAL: bold_red + log_text_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger():
    global logger

    # create logger
    logger = logging.getLogger('Extractor')
    # create console handler
    console_handler = logging.StreamHandler()
    # create formatter
    formatter = CustomFormatter()
    console_handler.setFormatter(formatter)
    # add console_handler to logger so it logs to console
    logger.addHandler(console_handler)

    logger.setLevel(logging.DEBUG)

    return logger


def Logger():
    global logger
    return logger


logger = setup_logger()



