import os

from .constants import API_RESPONSES_DIR

try:
    os.mkdir(API_RESPONSES_DIR)
except FileExistsError:
    pass
