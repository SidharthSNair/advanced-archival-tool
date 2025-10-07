from loguru import logger
import sys
from .config import settings

def configure_logging() -> None:
    # Remove default sink to avoid duplicate logs when reloading
    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        backtrace=False,
        diagnose=False,
        enqueue=True,  # safe for multi-threaded servers
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
    )
