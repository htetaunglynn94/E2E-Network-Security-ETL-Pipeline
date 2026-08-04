from datetime import datetime
import os
from network_security.constant import training_pipeline

# print(dir(training_pipeline))

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%Y_%m_%d_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir  = os.path.join(self.artifact_name, timestamp)
        self.timestamp:str = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Collect all file paths for Data Ingestion:
        - di_dir (for data ingestion directory)
        - fsfp (for feature store file path)
        - tin_fp (for train file path)
        - tst_fp (for test file path)
        - tts_ratio (train-tetst-split ratio)
        - collection_name (MongoDB collection name)
        - db_name (Database name)
        """ 

        self.di_dir:str = os.path.join(training_pipeline_config.artifact_dir, 
                                       training_pipeline.DI_DIR_NAME)
        self.fsfp:str = os.path.join(self.di_dir, 
                                     training_pipeline.DI_FEATURE_STORE_DIR,
                                     training_pipeline.FILE_NAME)
        self.tin_fp:str = os.path.join(self.di_dir, 
                                       training_pipeline.DI_INGESTED_DIR,
                                       training_pipeline.TRAIN_FILE_NAME)
        self.tst_fp:str = os.path.join(self.di_dir, 
                                       training_pipeline.DI_INGESTED_DIR,
                                       training_pipeline.TEST_FILE_NAME)
        self.tts_ratio:float = training_pipeline.DI_TTS_RATIO
        self.collection_name:str = training_pipeline.DI_COLLECTION_NAME
        self.db_name:str = training_pipeline.DI_DB_NAME

class DataValidationConfig:
    def __init__(self, training_pipeline_conf: TrainingPipelineConfig):
        """
        Collect all file paths for Data Validation:
        - dv_dir (for data validation directory)
        - vad_data_dir (for valid data directory)
        - invad_data_dir (for invalid data directory)
        - vad_tin_fp (for valid train data file path)
        - vad_tst_fp (for valid test data file path)
        - invad_tin_fp (for invalid train data file path)
        - invad_tst_fp (for invalid test data file path)
        - dft_report_fp (drift data report file path)
        """
        self.dv_dir:str = os.path.join(training_pipeline_conf.artifact_dir,
                                        training_pipeline.DV_DIR_NAME)
        self.vad_data_dir:str = os.path.join(self.dv_dir, 
                                                training_pipeline.DV_VALID_DIR)
        self.invad_data_dir:str = os.path.join(self.dv_dir,
                                                  training_pipeline.DV_INVALID_DIR)
        self.vad_tin_fp:str = os.path.join(self.vad_data_dir, 
                                           training_pipeline.TRAIN_FILE_NAME)
        self.vad_tst_fp:str = os.path.join(self.vad_data_dir, 
                                           training_pipeline.TEST_FILE_NAME)
        self.invad_tin_fp:str = os.path.join(self.invad_data_dir, 
                                             training_pipeline.TRAIN_FILE_NAME)
        self.invad_tst_fp:str = os.path.join(self.invad_data_dir, 
                                             training_pipeline.TEST_FILE_NAME)
        self.dft_report_fp:str = os.path.join(self.dv_dir, 
                                              training_pipeline.DV_DRIFT_REPORT_DIR, 
                                              training_pipeline.DV_DRIFT_REPORT_FILE_NAME)