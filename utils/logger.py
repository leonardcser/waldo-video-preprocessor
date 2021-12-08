import logging


class CustomFormatter(logging.Formatter):
    """
    CustomFormatter logger class that provides color output logging
    and custom formatting.
    """

    grey = "\x1b[38;21m"
    green = "\x1b[32;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[{levelname}] {message}"

    FORMATS = {
        "DEBUG": grey + format + reset,
        "INFO": grey + format + reset,
        "SUCCESS": green + format + reset,
        "WARNING": yellow + format + reset,
        "ERROR": red + format + reset,
        "CRITICAL": bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelname)
        message = record.getMessage()
        return log_fmt.format(levelname=record.levelname, message=message)


# create logger
logger = logging.getLogger("waldo-preprocess")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(CustomFormatter())
logger.addHandler(sh)

# set success level
logging.SUCCESS = 25  # between WARNING and INFO
logging.addLevelName(logging.SUCCESS, "SUCCESS")
setattr(
    logger,
    "success",
    lambda message, *args: logger._log(logging.SUCCESS, message, args),
)
