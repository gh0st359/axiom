import logging, sys
def get_logger(name: str = 'axiom-pro', level: int = logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    h = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter('[%(levelname)s] %(message)s')
    h.setFormatter(fmt)
    logger.addHandler(h)
    return logger
