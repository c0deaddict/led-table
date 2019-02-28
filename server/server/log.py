import logging

logger = logging.getLogger('server')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
