import os
import logging
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)
LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

fmt = "[%(asctime)s] line no:%(lineno)d-%(name)s-%(levelname)s-%(message)s"

logging.basicConfig(filename = LOG_FILE_PATH,
                    format = fmt,
                    level = logging.INFO)




