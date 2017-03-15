from logging.handlers import RotatingFileHandler
import logging
import os


def set_logger():

    log_path = os.path.join(os.getcwd(), "Logs")
    file_name = "news.log"
    size_50MB = 50000000
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except:
            pass
    full_path = os.path.join(log_path, file_name)
    logging.basicConfig(format='%(filename)s : %(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(full_path, maxBytes=size_50MB, backupCount=5)
    logger.addHandler(handler)
    formatter = logging.Formatter(fmt='%(filename)s : %(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
