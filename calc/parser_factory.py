import logging
import logging_config
from pathlib import Path

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

CONFIG_PATH = Path('calc.cfg')

def get_parser(config_path:Path=CONFIG_PATH) -> Parser:
    """
    """
    raise NotImplementedError()
