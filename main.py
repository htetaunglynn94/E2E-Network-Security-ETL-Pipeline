import sys
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.components.data_ingestion import DataIngestionConfig
from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig
from network_security.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        train_pipe_conf = TrainingPipelineConfig()
        di_conf = DataIngestionConfig(train_pipe_conf)
        di = DataIngestion(di_conf)
        logging.info("Initiate the data ingestion.")
        di_artifact = di.initiate_data_ingestion()
        logging.info("Data initiation completed successfully.")
        print(di_artifact)
        dv_conf = DataValidationConfig(train_pipe_conf)
        dv = DataValidation(di_artifact, dv_conf)
        logging.info("Initiate the data validation.")
        dv_artifact = dv.initiate_data_validation()
        logging.info("Data validation completed successfully.")
        print(dv_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
