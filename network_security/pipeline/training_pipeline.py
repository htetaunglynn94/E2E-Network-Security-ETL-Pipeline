import os, sys

from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_transformation import DataTransformation
from network_security.components.data_validation import DataValidation
from network_security.components.model_trainer import ModelTrainer

from network_security.entity.config_entity import ( TrainingPipelineConfig,
                                                    DataIngestionConfig,
                                                    DataValidationConfig,
                                                    DataTransformationConfig,
                                                    ModelTrainerConfig) 

from network_security.entity.artifact_entity import (DataIngestionArtifact,
                                                            DataValidationArtifact,
                                                            DataTransformationArtifact,
                                                            ClassificationMetricArtifact,
                                                            ModelTrainerArtifact)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_conf = TrainingPipelineConfig()

    # Start data ingestion
    def start_data_ingestion(self):
        try:
            self.data_ingestion_conf = DataIngestionConfig(self.training_pipeline_conf)
            logging.info("Start data ingestion")
            data_ingestion = DataIngestion(self.data_ingestion_conf)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data initiation completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact


        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Start data validation
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_conf = DataValidationConfig(self.training_pipeline_conf)
            data_validation = DataValidation(data_ingestion_artifact, data_validation_conf)
            logging.info("Initiate the data validation.")
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data validation completed and artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Start data transformation
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            data_transformation_conf = DataTransformationConfig(self.training_pipeline_conf)
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_conf)
            logging.info("Initiate the data transformation.")
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data transformation completed and artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    # Start model training
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_conf: ModelTrainerConfig = ModelTrainerConfig(self.training_pipeline_conf)
            model_trainer = ModelTrainer(data_transformation_artifact, model_trainer_conf)
            logging.info("Initiate the model training.")
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model training completed and artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Run pipeline
    def run_pipeline(self):
        try:
            di_artifact = self.start_data_ingestion()
            dv_artifact = self.start_data_validation(di_artifact)
            dt_artifact = self.start_data_transformation(dv_artifact)
            mt_artifact = self.start_model_training(dt_artifact)
            return mt_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)