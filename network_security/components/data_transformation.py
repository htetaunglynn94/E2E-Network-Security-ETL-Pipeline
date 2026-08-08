# Basic python libraries
import sys, os
import numpy as np
import pandas as pd

# Scikit-learn libraries
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.logging.logger import logging
from network_security.constant.training_pipeline import TARGET_COLUMN
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.config_entity import DataTransformationConfig
from network_security.entity.artifact_entity import (DataTransformationArtifact, 
                                                    DataValidationArtifact)
from network_security.constant.training_pipeline import DT_TRANSOFRMATION_IMPUTER_PARAS
from network_security.utils.main_utils.utils import save_objects, save_numpy_array_data

class DataTransformation:
    def __init__(self, 
                data_validation_artifact: DataValidationArtifact, 
                data_transformation_config: DataTransformationConfig):
        try:
            self.dv_artifact = data_validation_artifact
            self.dt_conf = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def read_data(self, file_path:str) -> pd.DataFrame:
        try:
            input_feature  = pd.read_csv(file_path).drop(columns=[TARGET_COLUMN])
            target_feature = pd.read_csv(file_path)[TARGET_COLUMN]
            target_feature = target_feature.replace(-1, 0) # Replacing -1 with 0 for binary classification
            return input_feature, target_feature

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformator_obj(self) -> Pipeline:
        """
        Initialize KNNImputer object with parameters specified in the constant file (training_pipeline/__init__.py).
        and returns a Pipeline object with KNNImputer as the first step.
        Args:
        class: DataTransformation

        Returns: Pipeline object
        """
        try:
            pass

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered the initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation process")
            train_ip_data, train_op_data = self.read_data(self.dv_artifact.valid_train_file_path)
            test_ip_data, test_op_data = self.read_data(self.dv_artifact.valid_test_file_path)


        except Exception as e:
            raise NetworkSecurityException(e, sys)