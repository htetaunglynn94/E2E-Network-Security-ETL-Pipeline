import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo 
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

ca = certifi.where() # certificate authority

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = (data.T.to_json())
        except Exception as e:
            raise NetworkSecurityException(e, sys)
