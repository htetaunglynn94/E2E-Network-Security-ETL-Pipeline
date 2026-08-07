import os, sys
import pandas as pd
from scipy.stats import ks_2samp

from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file
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
            if (len(missed_col) == 0) and (len(mistmatch_dtype) == 0):
                return True
            return False
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_sample_dist = ks_2samp(d1, d2) # compare the distributions of two samples
                
                if is_sample_dist.pvalue > threshold:
                    is_found = False
                else:
                    is_found = True

                report.update({col: {"pvalue": float(is_sample_dist.pvalue), 
                                     "drift_status": is_found}})
                
                drift_report_file_path = self.dv_conf.dft_report_fp
                drift_report_dir = os.path.dirname(drift_report_file_path)
                os.makedirs(drift_report_dir, exist_ok=True)
                write_yaml_file(drift_report_file_path, content=report)

        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.di_artifact.trained_file_path
            test_file_path  = self.di_artifact.test_file_path

            # Read train and test data
            train_df = DataValidation.read_data(train_file_path)
            test_df  = DataValidation.read_data(test_file_path)

            status = {"train":{"step1": None, "step2": None},
                      "test":{"step1": None, "step2": None}}

            # Validate number of columns
            status["train"]["step1"] = self.validate_num_of_cols(dataframe=train_df)
            if status["train"]["step1"]:
                logging.info("Train data contains all columns.\n")
            status["test"]["step1"] = self.validate_num_of_cols(dataframe=test_df)
            if status["test"]["step1"]:
                logging.info("Test data contains all columns.\n")

            # Validate data type of all columns
            status["train"]["step2"] = self.validate_numeric_cols(dataframe=train_df)
            if status["train"]["step2"]:
                logging.info("Data types in train data are matched.\n")
            status["test"]["step2"] = self.validate_numeric_cols(dataframe=test_df)
            if status["test"]["step2"]:
                logging.info("Data types in test data are matched.\n")

            # dir_path = os.path.dirname(self.dv_conf.dft_report_fp)
            # os.makedirs(dir_path, exist_ok=True)
            os.makedirs(self.dv_conf.dft_report_fp, exist_ok=True)
            os.makedirs(self.dv_conf.vad_data_dir, exist_ok=True)
            os.makedirs(self.dv_conf.invad_data_dir, exist_ok=True)
            print(status)
            if status["train"]["step1"] and status["train"]["step2"] and status["test"]["step1"] and status["test"]["step2"]:
                train_df.to_csv(self.dv_conf.vad_tin_fp, index=False, header=True)
                test_df.to_csv(self.dv_conf.vad_tst_fp, index=False, header=True)
            else:
                train_df.to_csv(self.dv_conf.invad_tin_fp, index=False, header=True)
                test_df.to_csv(self.dv_conf.invad_tst_fp, index=False, header=True)

            dv_artifact = DataValidationArtifact(
                            validation_status = status,
                            valid_train_file_path = self.di_artifact.trained_file_path,
                            valid_test_file_path = self.di_artifact.test_file_path,
                            invalid_train_file_path = None,
                            invalid_test_file_path = None,
                            drift_report_file_path = self.dv_conf.dft_report_fp
                            )
            return dv_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)



