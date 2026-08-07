import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from dotenv import load_dotenv

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

# Configure Data Ingestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact

# Import scikit-learn libraries
from sklearn.model_selection import train_test_split as TTS

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Read data from MongoDB collection and return as pandas DataFrame.
        """
        try:
            db_name = self.data_ingestion_config.db_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df = df.drop(columns=['_id'])
            df.replace({'na': np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.fsfp
            # Create directory
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
            train_set, test_set = TTS(dataframe, test_size=self.data_ingestion_config.tts_ratio, random_state=42)
            
            logging.info("Performed train-test split on dataframe.")
            logging.info("Exited split_data_as_train_test method of Data Ingestion class.")

            self.train_path = self.data_ingestion_config.tin_fp
            self.test_path = self.data_ingestion_config.tst_fp

            # Create directory
            train_dir_path = os.path.dirname(self.train_path)
            os.makedirs(train_dir_path, exist_ok=True)
            test_dir_path = os.path.dirname(self.test_path)
            os.makedirs(test_dir_path, exist_ok=True)

            logging.info("Exporting train and test file path.")

            train_set.to_csv(self.train_path, index=False, header=True)
            test_set.to_csv(self.test_path, index=False, header=True)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
                                            trained_file_path = self.train_path,
                                            test_file_path = self.test_path)
            return dataingestionartifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
