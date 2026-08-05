import os, sys
import pandas as pd
from scipy.stats import ks_2samp

from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import read_yaml_file
from network_security.entity.config_entity import DataValidationConfig
from network_security.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security.entity.artifact_entity import DataIngestionArtifact
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.artifact_entity import DataValidationArtifact

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

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_num_of_cols(self, dataframe:pd.DataFrame) -> bool:
        try:
            num_of_cols = len(self._schema_conf)
            logging.info(f"Required number of columns: {num_of_cols}")
            logging.info(f"Data frame has {len(dataframe.columns)} columns.")
            if len(dataframe.columns) == num_of_cols:
                return True

            return False

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_numeric_cols(self, dataframe:pd.DataFrame) -> bool:
        try:
            df = dataframe
            schema = self._schema_conf.get("columns_dtypes", {})
            schema_dct = {col: dtype for item in schema for col, dtype in item.items()}
            missed_col = [col for col in schema_dct if col not in df.columns]
            mistmatch_dtype = [col for col, exp_type in schema_dct.items() if exp_type != str(df[col].dtype)]
            logging.info(f"Missed columns: {len(missed_col)} | Type mismatches: {len(mistmatch_dtype)}")
            if (missed_col == 0) and (mistmatch_dtype == 0):
                return True
            return False
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self):
        try:
            pass
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.di_artifact.trained_file_path
            test_file_path  = self.di_artifact.test_file_path

            # Read train and test data
            train_df = DataValidation.read_data(train_file_path)
            test_df  = DataValidation.read_data(test_file_path)

            # Validate number of columns
            status = self.validate_num_of_cols(dataframe=train_df)
            if not status:
                error_msg = "Train data does not contain all columns.\n"
            status = self.validate_num_of_cols(dataframe=test_df)
            if not status:
                error_msg = "Test data does not contain all columns.\n"

            # Validate data type of all columns
            status = DataValidation.validate_numeric_cols(dataframe=train_df)
            if not status:
                error_msg = "Data types in train data are not matched.\n"
            status = DataValidation.validate_numeric_cols(dataframe=test_df)
            if not status:
                error_msg = "Data types in test data are not matched.\n"

            # Check data drift


        except Exception as e:
            raise NetworkSecurityException(e, sys)



