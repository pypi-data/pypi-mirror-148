import logging

__version__ = "0.1.3"

logging.getLogger("kedro-io").addHandler(logging.NullHandler())
