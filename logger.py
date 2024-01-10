import sys
import logging
logger = logging.getLogger(__name__)
stdout = logging.StreamHandler(stream=sys.stdout)
fmt = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
stdout.setFormatter(fmt)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)
