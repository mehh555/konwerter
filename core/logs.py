import logging
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / "konwerter.log"


def setup_logging():
    logging.basicConfig(filename=LOG_FILE, encoding="utf-8", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")