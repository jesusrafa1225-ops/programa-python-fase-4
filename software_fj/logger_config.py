import logging
from pathlib import Path

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler(Path(__file__).resolve().parent.parent / "software_fj.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
