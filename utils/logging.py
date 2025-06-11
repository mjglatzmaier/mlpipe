from loguru import logger

# TODO
logger.add("logs/pipeline.log", rotation="1 MB", level="INFO")