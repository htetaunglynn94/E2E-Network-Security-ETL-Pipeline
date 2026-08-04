import os, sys
import pandas as pd
from scipy.stats import ks_2samp

from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import read_yaml_file
from network_security.entity.config_entity import DataValidationConfig
from network_security.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security.entity.artifact_entity import DataIngestionArtifact
from network_security.exception.exception import NetworkSecurityException



class DataValidation:
    def __init__(self, 
                 data_ingestion_artifact: DataIngestionArtifact, 
                 data_validation_config: DataValidationConfig):
        try:
            self.di_artifact = data_ingestion_artifact
            self.dv_conf = data_validation_config
            self._schema_conf = read_yaml_file(SCHEMA_FILE_PATH)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)



