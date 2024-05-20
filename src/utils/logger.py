import logging


def setup_logger(name, level=logging.INFO) -> logging.Logger:
    time_format = "%d.%m.%Y %I:%M:%S %p"
    filename = "D:\\projects\\VKR\\logs\\users.log"
    logging.basicConfig(datefmt=time_format, level=level, filename=filename)
    logger = logging.getLogger(name)
    return logger
