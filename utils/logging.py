from loguru import logger

logger.add("logs/pipeline.log", rotation="1 MB", level="INFO")