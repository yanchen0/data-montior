import logging,os
def init_logger(name=None, log_file=None):
    from logging import Formatter
    from logging.handlers import RotatingFileHandler
    import sys

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not log_file:
        log_file = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0], name + '.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(Formatter('%(asctime)s\t%(levelname)s\t%(message)s'))
    logger.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.ERROR)
    stdout_handler.setFormatter(Formatter('%(asctime)s\t%(levelname)s\t%(message)s'))
    logger.addHandler(stdout_handler)

    return logger
logger = init_logger(__name__, os.path.join(os.path.split(os.path.abspath(__file__))[0], __name__ + '.log'))