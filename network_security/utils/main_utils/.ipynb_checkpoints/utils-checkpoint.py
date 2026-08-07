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

def write_yaml_file(file_path:str, content:object, replace:bool=False) -> None:
    try:
        if os.path.isdir(file_path):
            os.rmdir(file_path)
            
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as yf:
            yaml.dump(content, yf)

    except Exception as e:
        raise NetworkSecurityException(e, sys)