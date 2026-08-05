import numpy as np
import os, sys, yaml, dill, pickle

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yf:
            return yaml.safe_load(yf)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)