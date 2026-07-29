import os
import sys
from network_security.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        # Get full file path
        full_path = exc_tb.tb_frame.f_code.co_filename
        # Shorten to relative path from current working directory
        self.file_name = os.path.relpath(full_path, os.getcwd())
        self.line_no = exc_tb.tb_lineno

    def __str__(self):
        return "Error occurred in file name:{1}-line no:{0}-message:{2}" \
            .format(self.line_no, self.file_name, self.error_message)

# if __name__ == "__main__":
#     try:
#         logger.logging.info("Start calculation...")
#         a = 1/0
#         print("This one will not be printed", a)
#     except Exception as e:
#         raise NetworkSecurityException(e, sys)