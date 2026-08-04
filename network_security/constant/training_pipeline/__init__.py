# Constant Information for DATA INGESTION
import os

## Define common constant variable for training pipeline

TARGET_COLUMN = "Result"                 # dependent feature to predict
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "artifacts"
FILE_NAME:str = "phisingData.csv"       # raw data file
TRAIN_FILE_NAME:str = "train.csv"       # traiining data file
TEST_FILE_NAME:str = "test.csv"         # testing data file
SCHEMA_FILE_PATH:str = os.path.join("data_schema", "schema.yaml")

## Data ingestion related constant start with DI VAR NAME

DI_COLLECTION_NAME:str = "NetworkData"
DI_DB_NAME:str = "HtetAungLynn"
DI_DIR_NAME:str = "data_ingestion"
DI_FEATURE_STORE_DIR:str = "feature_store"
DI_INGESTED_DIR:str = "ingested"           
DI_TTS_RATIO:float = 0.2      # tain-test-split ratio

## Data validation related constant start with DV VAR NAME
DV_DIR_NAME:str = "data_validation"
DV_VALID_DIR:str = "validated"
DV_INVALID_DIR:str = "invalid"
DV_DRIFT_REPORT_DIR:str = "drift_report"
DV_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

