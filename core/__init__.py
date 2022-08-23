import os
import logger

from .constants import API_RESPONSES_DIR

try:
    os.mkdir(API_RESPONSES_DIR)
except Exception as e:
    logger.get_logger().info(f"Cannot create {API_RESPONSES_DIR} directory because of - {e}")

